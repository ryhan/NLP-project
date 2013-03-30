//
// StanfordCoreNLP -- a suite of NLP tools
// Copyright (c) 2009-2010 The Board of Trustees of
// The Leland Stanford Junior University. All Rights Reserved.
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
//
// For more information, bug reports, fixes, contact:
//    Christopher Manning
//    Dept of Computer Science, Gates 1A
//    Stanford CA 94305-9010
//    USA
//

package edu.stanford.nlp.dcoref;

import java.io.Serializable;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeMap;
import java.util.logging.Logger;

import edu.stanford.nlp.dcoref.Dictionaries.Animacy;
import edu.stanford.nlp.dcoref.Dictionaries.Gender;
import edu.stanford.nlp.dcoref.Dictionaries.MentionType;
import edu.stanford.nlp.dcoref.Dictionaries.Number;
import edu.stanford.nlp.dcoref.Semantics;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;

/**
 * One cluster for the SieveCoreferenceSystem.
 *
 * @author Heeyoung Lee
 */
public class CorefCluster implements Serializable{

  private static final long serialVersionUID = 8655265337578515592L;
  protected Set<Mention> corefMentions;
  protected int clusterID;

  // Attributes for cluster - can include multiple attribute e.g., {singular, plural}
  protected Set<Number> numbers;
  protected Set<Gender> genders;
  protected Set<Animacy> animacies;
  protected Set<String> nerStrings;
  protected Set<String> heads;

  /** All words in this cluster - for word inclusion feature  */
  public Set<String> words;

  /** The first mention in this cluster */
  protected Mention firstMention;
  
  /** Return the most representative mention in the chain. 
   *  Proper mention and a mention with more pre-modifiers are preferred.  
   */
  protected Mention representative;

  public int getClusterID(){ return clusterID; }
  public Set<Mention> getCorefMentions() { return corefMentions; }
  public Mention getFirstMention() { return firstMention; }
  public Mention getRepresentativeMention() { return representative; }

  public CorefCluster(int ID) {
    clusterID = ID;
    corefMentions = new HashSet<Mention>();
    numbers = EnumSet.noneOf(Number.class);
    genders = EnumSet.noneOf(Gender.class);
    animacies = EnumSet.noneOf(Animacy.class);
    nerStrings = new HashSet<String>();
    heads = new HashSet<String>();
    words = new HashSet<String>();
    firstMention = null;
    representative = null;
  }

  public CorefCluster(){
    this(-1);
  }

  public CorefCluster(int ID, Set<Mention> mentions){
    this(ID);
    corefMentions.addAll(mentions);
    for(Mention m : mentions){
      animacies.add(m.animacy);
      genders.add(m.gender);
      numbers.add(m.number);
      nerStrings.add(m.nerString);
      heads.add(m.headString);
      if(!m.isPronominal()){
        for(CoreLabel w : m.originalSpan){
          words.add(w.get(TextAnnotation.class).toLowerCase());
        }
      }
      if(firstMention == null) firstMention = m;
      else {
        if(m.appearEarlierThan(firstMention)) firstMention = m;
      }
    }
    representative = firstMention;
    for(Mention m : mentions) {
      if(m.moreRepresentativeThan(representative)) representative = m;
    }
  }

  /** merge 2 clusters: to = to + from */
  public static void mergeClusters(CorefCluster to, CorefCluster from) {
    int toID = to.clusterID;
    for (Mention m : from.corefMentions){
      m.corefClusterID = toID;
    }
    if(Constants.SHARE_ATTRIBUTES){
      to.numbers.addAll(from.numbers);
      if(to.numbers.size() > 1 && to.numbers.contains(Number.UNKNOWN)) {
        to.numbers.remove(Number.UNKNOWN);
      }

      to.genders.addAll(from.genders);
      if(to.genders.size() > 1 && to.genders.contains(Gender.UNKNOWN)) {
        to.genders.remove(Gender.UNKNOWN);
      }

      to.animacies.addAll(from.animacies);
      if(to.animacies.size() > 1 && to.animacies.contains(Animacy.UNKNOWN)) {
        to.animacies.remove(Animacy.UNKNOWN);
      }

      to.nerStrings.addAll(from.nerStrings);
      if(to.nerStrings.size() > 1 && to.nerStrings.contains("O")) {
        to.nerStrings.remove("O");
      }
      if(to.nerStrings.size() > 1 && to.nerStrings.contains("MISC")) {
        to.nerStrings.remove("MISC");
      }
    }

    to.heads.addAll(from.heads);
    to.corefMentions.addAll(from.corefMentions);
    to.words.addAll(from.words);
    if(from.firstMention.appearEarlierThan(to.firstMention) && !from.firstMention.isPronominal()) to.firstMention = from.firstMention;
    if(from.representative.moreRepresentativeThan(to.representative)) to.representative = from.representative;
    SieveCoreferenceSystem.logger.finer("merge clusters: "+toID+" += "+from.clusterID);
  }
  public static boolean personDisagree(Document document, CorefCluster mentionCluster, CorefCluster potentialAntecedent, Dictionaries dict){
    boolean disagree = false;
    for(Mention m : mentionCluster.getCorefMentions()) {
      for(Mention ant : potentialAntecedent.getCorefMentions()) {
        if(Mention.personDisagree(document, m, ant, dict)) {
          disagree = true;        
        }
      }
    }
    if(disagree) return true;
    else return false;
  }
  /** Word inclusion except stop words  */
  public static boolean wordsIncluded(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Mention mention, Mention ant) {
    Set<String> wordsExceptStopWords = new HashSet<String>(mentionCluster.words);
    wordsExceptStopWords.removeAll(Arrays.asList(new String[]{ "the","this", "mr.", "miss", "mrs.", "dr.", "ms.", "inc.", "ltd.", "corp.", "'s"}));
    wordsExceptStopWords.remove(mention.headString.toLowerCase());
    if(potentialAntecedent.words.containsAll(wordsExceptStopWords)) return true;
    else return false;
  }

  /** Compatible modifier only  */
  public static boolean haveIncompatibleModifier(CorefCluster mentionCluster, CorefCluster potentialAntecedent) {
    for(Mention m : mentionCluster.corefMentions){
      for(Mention ant : potentialAntecedent.corefMentions){
        if(m.haveIncompatibleModifier(ant)) return true;
      }
    }
    return false;
  }
  public static boolean isRoleAppositive(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Mention m1, Mention m2, Dictionaries dict) {
    if(!attributesAgree(mentionCluster, potentialAntecedent)) return false;
	  return m1.isRoleAppositive(m2, dict) || m2.isRoleAppositive(m1, dict);
  }
  public static boolean isRelativePronoun(Mention m1, Mention m2) {
	    return m1.isRelativePronoun(m2) || m2.isRelativePronoun(m1);
	}

  public static boolean isAcronym(CorefCluster mentionCluster, CorefCluster potentialAntecedent) {
    for(Mention m : mentionCluster.corefMentions){
      if(m.isPronominal()) continue;
      for(Mention ant : potentialAntecedent.corefMentions){
        if(m.isAcronym(ant) || ant.isAcronym(m)) return true;
      }
    }
    return false;
  }

  public static boolean isPredicateNominatives(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Mention m1, Mention m2) {
    if(!attributesAgree(mentionCluster, potentialAntecedent)) return false;
    if ((m1.startIndex <= m2.startIndex && m1.endIndex >= m2.endIndex)
            || (m1.startIndex >= m2.startIndex && m1.endIndex <= m2.endIndex)) {
      return false;
    }
    return m1.isPredicateNominatives(m2) || m2.isPredicateNominatives(m1);
  }

  public static boolean isApposition(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Mention m1, Mention m2) {
    if(!attributesAgree(mentionCluster, potentialAntecedent)) return false;
    if(m1.mentionType==MentionType.PROPER && m2.mentionType==MentionType.PROPER) return false;
    if(m1.nerString.equals("LOCATION")) return false;
    return m1.isApposition(m2) || m2.isApposition(m1);
	}

  public static boolean attributesAgree(CorefCluster mentionCluster, CorefCluster potentialAntecedent){
    
    boolean hasExtraAnt = false;
    boolean hasExtraThis = false;

    // number
    if(!mentionCluster.numbers.contains(Number.UNKNOWN)){
      for(Number n : potentialAntecedent.numbers){
        if(n!=Number.UNKNOWN && !mentionCluster.numbers.contains(n)) hasExtraAnt = true;
      }
    }
    if(!potentialAntecedent.numbers.contains(Number.UNKNOWN)){
      for(Number n : mentionCluster.numbers){
        if(n!=Number.UNKNOWN && !potentialAntecedent.numbers.contains(n)) hasExtraThis = true;
      }
    }

    if(hasExtraAnt && hasExtraThis) return false;

    // gender
    hasExtraAnt = false;
    hasExtraThis = false;

    if(!mentionCluster.genders.contains(Gender.UNKNOWN)){
      for(Gender g : potentialAntecedent.genders){
        if(g!=Gender.UNKNOWN && !mentionCluster.genders.contains(g)) hasExtraAnt = true;
      }
    }
    if(!potentialAntecedent.genders.contains(Gender.UNKNOWN)){
      for(Gender g : mentionCluster.genders){
        if(g!=Gender.UNKNOWN && !potentialAntecedent.genders.contains(g)) hasExtraThis = true;
      }
    }
    if(hasExtraAnt && hasExtraThis) return false;

    // animacy
    hasExtraAnt = false;
    hasExtraThis = false;

    if(!mentionCluster.animacies.contains(Animacy.UNKNOWN)){
      for(Animacy a : potentialAntecedent.animacies){
        if(a!=Animacy.UNKNOWN && !mentionCluster.animacies.contains(a)) hasExtraAnt = true;
      }
    }
    if(!potentialAntecedent.animacies.contains(Animacy.UNKNOWN)){
      for(Animacy a : mentionCluster.animacies){
        if(a!=Animacy.UNKNOWN && !potentialAntecedent.animacies.contains(a)) hasExtraThis = true;
      }
    }
    if(hasExtraAnt && hasExtraThis) return false;

    // NE type
    hasExtraAnt = false;
    hasExtraThis = false;

    if(!mentionCluster.nerStrings.contains("O") && !mentionCluster.nerStrings.contains("MISC")){
      for(String ne : potentialAntecedent.nerStrings){
        if(!ne.equals("O") && !ne.equals("MISC") && !mentionCluster.nerStrings.contains(ne)) hasExtraAnt = true;
      }
    }
    if(!potentialAntecedent.nerStrings.contains("O") && !potentialAntecedent.nerStrings.contains("MISC")){
      for(String ne : mentionCluster.nerStrings){
        if(!ne.equals("O") && !ne.equals("MISC") && !potentialAntecedent.nerStrings.contains(ne)) hasExtraThis = true;
      }
    }
    return ! (hasExtraAnt && hasExtraThis);
  }

  public static boolean relaxedHeadsAgreeBetweenMentions(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Mention m, Mention ant) {
    if(m.isPronominal() || ant.isPronominal()) return false;
    if(m.headsAgree(ant)) return true;
    return false;
  }

  public static boolean headsAgree(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Mention m, Mention ant, Dictionaries dict) {
    boolean headAgree = false;
    if(m.isPronominal() || ant.isPronominal()
        || dict.allPronouns.contains(m.spanToString().toLowerCase())
        || dict.allPronouns.contains(ant.spanToString().toLowerCase())) return false;
    for(Mention a : potentialAntecedent.corefMentions){
      if(a.headString.equals(m.headString)) headAgree= true;
    }
    return headAgree;
  }

  public static boolean exactStringMatch(CorefCluster mentionCluster, CorefCluster potentialAntecedent, Dictionaries dict, Set<Mention> roleSet){
    boolean matched = false;
    for(Mention m : mentionCluster.corefMentions){
      if(roleSet.contains(m)) return false;
      for(Mention ant : potentialAntecedent.corefMentions){

        String mSpan = m.spanToString().toLowerCase();
        String antSpan = ant.spanToString().toLowerCase();
        
        if(m.isPronominal() || ant.isPronominal()
            || dict.allPronouns.contains(mSpan)
            || dict.allPronouns.contains(antSpan)) continue;
        if(mSpan.equals(antSpan)) matched = true;
        if(mSpan.equals(antSpan+" 's") || antSpan.equals(mSpan+" 's")) matched = true;
        
      }
    }
    return matched;
  }

  /**
   * Exact string match except phrase after head (only for proper noun):
   * For dealing with a error like "[Mr. Bickford] <- [Mr. Bickford , an 18-year mediation veteran]"
   */
  public static boolean relaxedExactStringMatch(
      CorefCluster mentionCluster,
      CorefCluster potentialAntecedent,
      Mention mention,
      Mention ant,
      Dictionaries dict,
      Set<Mention> roleSet){
    if(roleSet.contains(mention)) return false;
    if(mention.isPronominal() || ant.isPronominal()
        || dict.allPronouns.contains(mention.spanToString().toLowerCase())
        || dict.allPronouns.contains(ant.spanToString().toLowerCase())) return false;
    String mentionSpan = mention.removePhraseAfterHead();
    String antSpan = ant.removePhraseAfterHead();
    if(mentionSpan.equals("") || antSpan.equals("")) return false;

    if(mentionSpan.equals(antSpan) || mentionSpan.equals(antSpan+" 's") || antSpan.equals(mentionSpan+" 's")){
      return true;
    }
    return false;
  }

  /** Print cluster information */
  public void printCorefCluster(Logger logger){
    logger.finer("Cluster ID: "+clusterID+"\tNumbers: "+numbers+"\tGenders: "+genders+"\tanimacies: "+animacies);
    logger.finer("NE: "+nerStrings+"\tfirst Mention's ID: "+firstMention.mentionID+"\tHeads: "+heads+"\twords: "+words);
    TreeMap<Integer, Mention> forSortedPrint = new TreeMap<Integer, Mention>();
    for(Mention m : this.corefMentions){
      forSortedPrint.put(m.mentionID, m);
    }
    for(Mention m : forSortedPrint.values()){
      if(m.goldCorefClusterID==-1){
        logger.finer("mention-> id:"+m.mentionID+"\toriginalRef: "+m.originalRef+"\t"+m.spanToString() +"\tsentNum: "+m.sentNum+"\tstartIndex: "+m.startIndex);
      } else{
        logger.finer("mention-> id:"+m.mentionID+"\toriginalClusterID: "+m.goldCorefClusterID+"\t"+m.spanToString() +"\tsentNum: "+m.sentNum+"\tstartIndex: "+m.startIndex +"\toriginalRef: "+m.originalRef+"\tType: "+m.mentionType);
      }
    }
  }

  public boolean isSinglePronounCluster(Dictionaries dict){
    if(this.corefMentions.size() > 1) return false;
    for(Mention m : this.corefMentions) {
      if(m.isPronominal() || dict.allPronouns.contains(m.spanToString().toLowerCase())) return true;
    }
    return false;
  }
  public static boolean bothHaveProper(CorefCluster mentionCluster,
      CorefCluster potentialAntecedent) {
    boolean mentionClusterHaveProper = false;
    boolean potentialAntecedentHaveProper = false;
    
    for (Mention m : mentionCluster.corefMentions) {
      if (m.mentionType==MentionType.PROPER) {
        mentionClusterHaveProper = true;
      }
    }
    for (Mention a : potentialAntecedent.corefMentions) {
      if (a.mentionType==MentionType.PROPER) {
        potentialAntecedentHaveProper = true;
      }
    }
    return (mentionClusterHaveProper && potentialAntecedentHaveProper);
  }
  public static boolean sameProperHeadLastWord(CorefCluster mentionCluster,
      CorefCluster potentialAntecedent, Mention mention, Mention ant) {
    for (Mention m : mentionCluster.getCorefMentions()){
      for (Mention a : potentialAntecedent.getCorefMentions()) {
        if (Mention.sameProperHeadLastWord(m, a)) return true;
      }
    }
    return false;
  }
  
  public static boolean alias(CorefCluster mentionCluster, CorefCluster potentialAntecedent,
      Semantics semantics, Dictionaries dict) throws Exception {
    
    Mention mention = mentionCluster.getRepresentativeMention();
    Mention antecedent = potentialAntecedent.getRepresentativeMention();
    if(mention.mentionType!=MentionType.PROPER
        || antecedent.mentionType!=MentionType.PROPER) return false;
    
    Method meth = semantics.wordnet.getClass().getMethod("alias", new Class[]{Mention.class, Mention.class});
    if((Boolean) meth.invoke(semantics.wordnet, new Object[]{mention, antecedent})) {
      return true;
    }
    return false;
  }
  public static boolean iWithini(CorefCluster mentionCluster,
      CorefCluster potentialAntecedent, Dictionaries dict) {
    for(Mention m : mentionCluster.getCorefMentions()) {
      for(Mention a : potentialAntecedent.getCorefMentions()) {
        if(Mention.iWithini(m, a, dict)) return true;
      }
    }
    return false;
  }
}
