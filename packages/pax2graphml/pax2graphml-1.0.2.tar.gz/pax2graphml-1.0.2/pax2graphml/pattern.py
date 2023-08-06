import logging
import copy

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PatternList:

   def __init__(self):
        self.plist = list()
   def add(self,p):
        pc=copy.deepcopy(p)
        self.plist.append(pc)
   def generate(self):
       code=""
       ix=0
       for p in self.plist:
           ix+=1
           if p.mname is None or p.mname == "":
              p.mname="custompattern%s" %(ix)
           code+=p.generate(p.mname)  +p.eol
           code+="%s" %(p.eol)
       code+="%s" %(p.eol)
       code+="public static ArrayList  plist(){%s" %(p.eol)
       for p in self.plist:
           code+="   patternList.add(%s());%s" %(p.mname,p.eol)
       code+="   return patternList;%s" %(p.eol)
       code+="}%s" %(p.eol)
       return code

class Pattern:

   def __init__(self,clazz=None,name="pattern"):
        self.code = ""
        self.clazz=clazz
        self.name=name
        self.mname=None
        self.eol="\n"
        self.elements=list()


   def add(self,fct,nameMember1="mb1",nameMember2="mb2", nameMember3=None):
       if isinstance(fct, (list)):
          fctcontent=fct[0]
          mode=fct[1]
       else:
          fctcontent=fct
          mode=0

       if mode==0:
           if nameMember3 is None:
             el="%sadd(%s,\"%s\",\"%s\")" %(self.px(),fctcontent,nameMember1,nameMember2)     
           else:
             el="%sadd(%s,\"%s\",\"%s\",\"%s\")" %(self.px(),fctcontent,nameMember1,nameMember2,nameMember3)  
       else:
           el="%sadd(%s,\"%s\")" %(self.px(),fctcontent,nameMember1)

       self.elements.append(el)

   def ident(self,nb=1):

       tb=""
       t=" "
       for i in range(0,nb):
           tb+=t
       return tb


   def generate(self,mname="custompattern1"):
        self.code=self.ident(1)+"public static Pattern %s(){%s" %(mname,self.eol)

        self.code+=self.ident(2)+"Pattern p = new Pattern(%s.class, \"%s\");%s" %(self.clazz,self.name,self.eol)
        self.code+="  BoxWrapper a = new BoxWrapper(p);%s" %(self.eol)
        for el in self.elements:
            self.code+=self.ident(2)+"%s;%s"%(el,self.eol)
        self.code+=self.ident(2)+"return %sgetPattern();%s" \
                %(self.px(),self.eol)
        self.code+=self.ident(1)+"}%s"%(self.eol)

        return self.code


   def b2s(self,b):
       if b==None:
         b=False
       if b==True:
            bstr="true"
       else:
            bstr="false"
       return bstr

   def px(self):
       return "a."

   def linkedER(self,b=True):
        bstr=self.b2s(b)
        return "%slinkedER(%s)" %(self.px(),bstr)

   def erToPE(self):
        return "%serToPE()" % (self.px()) 

   def linkToComplex(self):
        return "%slinkToComplex()" % (self.px())

   def peToControl(self):
       return "%speToControl()" % (self.px())

   def controlToTempReac(self):
       return "%scontrolToTempReac()" % (self.px())

   def product(self):
       return "%sproduct()" %(self.px())

   def linkToSpecific(self):
       return "%slinkToSpecific()" %(self.px())

   def type(self,cls):
       lst=list()
       s="%stype(%s.class)"%(self.px(),cls)
       lst.append(s)
       lst.append(1)
       return lst

   def peToER(self):
       return "%speToER()" %(self.px())

   def equal(self,b=None):
       bstr=self.b2s(b)
       return "%sequal(%s)" %(self.px(),bstr)

   def controlToConv(self):
       return "%scontrolToConv()" %(self.px())

   def right(self):
       return "%sright()" %(self.px())

   def left(self):
       return "%sleft()" %(self.px())

   def size(self,c, sz, mode=None):
       m=mode
       if mode is None or mode.lower() =="equal":
          m="EQUAL"
          
       st= "%ssize(%s,%s,\"%s\")" %(self.px(),c,sz,m)
       return st
   def OR(self,mc1,mc2):
       st= "%sor(%s,%s)" %(self.px(),mc1,mc2)
       return st
   def NOT(self,mc1):
       st= "%snot(%s)" %(self.px(),mc1)
       return st
   def mappedConst(self,c,ix):
       st= "%smappedConst(%s,%s)" %(self.px(),c,ix)
       return st
   def empty(self,c):
       st= "%sempty(%s)" %(self.px(),c)
       return st
   def conversionMC(self):
       st= "%sconversionMC()" %(self.px())
       return st
   def participantER(self):
       st= "%sparticipantER()" %(self.px())
       return st
   def participant(self,rt,b=True):
       if rt is None or rt.lower()=="input":
          rt="INPUT" 
       
       st= "%sparticipant(\"%s\", %s)" %(self.px(),rt,self.b2s(b))
       return st

   def conversionSide(self,rt):
      if rt is None or rt.lower()=="other_side":
          rt="OTHER_SIDE"
      st= "%sconversionSide(\"%s\")" %(self.px(),rt)
      return st

   def modificationChangeConstraint(self,mc,lb):
      if mc is None or mc.lower()=="any":
          mc="ANY"
      st= "%smodificationChangeConstraint(\"%s\", \"%s\")" %(self.px(),mc,lb)
      return st

#controlsStateChange
def controlsStateChange():
 p = Pattern("SequenceEntityReference","controller ER")

 p.add(p.linkedER(True), "controller ER", "TF generic controllerER")
 p.add(p.erToPE(), "generic controller ER", "controller simple PE")
 p.add(p.linkToComplex(), "controller simple PE", "controller PE")
 p.add(p.peToControl(), "controller PE", "Control")
 p.add(p.controlToConv(), "Control", "Conversion")
 p.add(p.NOT(p.participantER()), "Conversion", "controller ER")
 p.add(p.participant("INPUT", True), "Control","Conversion", "input PE")
 p.add(p.linkToSpecific(), "input PE", "input simple PE")
 p.add(p.type("SequenceEntity"), "input simple PE")
 p.add(p.peToER(), "input simple PE", "changed generic ER")
 p.add(p.conversionSide("OTHER_SIDE"), "input PE", "Conversion", "output PE")
 p.add(p.equal(False), "input PE", "output PE")
 p.add(p.linkToSpecific(), "output PE", "output simple PE")
 p.add(p.peToER(), "output simple PE", "changed generic ER")
 p.add(p.linkedER(False), "changed generic ER", "changed ER")
 return p





pl= PatternList()

#controlsExpressionWithTemplateReac
p = Pattern("SequenceEntityReference","TF ER")
p.add(p.linkedER(True), "TF ER", "TF generic ER")
p.add(p.erToPE(), "TF generic ER", "TF SPE")
p.add(p.linkToComplex(), "TF SPE", "TF PE")
p.add(p.peToControl(), "TF PE", "Control")
p.add(p.controlToTempReac(), "Control", "TempReac")
p.add(p.product(), "TempReac", "product PE")
p.add(p.linkToSpecific(), "product PE", "product SPE")
p.add(p.type("SequenceEntity"), "product SPE")
p.add(p.peToER(), "product SPE", "product generic ER")
p.add(p.linkedER(False), "product generic ER", "product ER")
p.add(p.equal(False), "TF ER", "product ER")

pl.add(p)

#controlsExpressionWithConversion
p = Pattern("SequenceEntityReference","TF ER")
p.add(p.linkedER(True), "TF ER", "TF generic ER")
p.add(p.erToPE(), "TF generic ER", "TF SPE")
p.add(p.linkToComplex(), "TF SPE", "TF PE")
p.add(p.peToControl(), "TF PE", "Control")
p.add(p.controlToConv(), "Control", "Conversion")

p.add(p.size(p.right(), 1, "EQUAL"), "Conversion")

p.add(p.OR(p.mappedConst(p.empty(p.left()), 0),p.conversionMC()),"Conversion")
p.add(p.right(), "Conversion", "right PE")
p.add(p.linkToSpecific(), "right PE", "right SPE")
p.add(p.type("SequenceEntity"), "right SPE")
p.add(p.peToER(), "right SPE", "product generic ER")
p.add(p.linkedER(False), "product generic ER", "product ER")
p.add(p.equal(False), "TF ER", "product ER")
pl.add(p)


#controlsPhosphorylation()
p = controlsStateChange()

p.add(p.NOT(p.linkToSpecific()), "input PE", "output simple PE")
p.add(p.NOT(p.linkToSpecific()), "output PE", "input simple PE")
p.add(p.modificationChangeConstraint("ANY","phospho"), "input simple PE", "output simple PE")

pl.add(p)


code=pl.generate()
print(code)


