#!/usr/bin/python
#-*- encoding: Latin-1 -*-

#-------------------------------------------------------------------------------
# Name:         export
# Purpose:      A script to extract information from a MAppleT simulation for exportation.
# Author:       Da Silva
# Created:      03/26/2014
# Copyright:    (c) Da Silva 2014
# Licence:      CeCill/LGPL
#-------------------------------------------------------------------------------
from openalea.mtg.aml import *
from math import pi

import random
import openalea.plantgl.all as pgl
import os.path as op

#===========================================================#
# Utils functions to explore and extract data from MTG      #
#===========================================================#


#**************
# Access to Feature
#**************
def an(x):
  """
    Returns the year of growht of elmt x
  """
  return Feature(x, "year")
 
def radius(x) :
  """
  Return the radius [m]
  """
  return Feature(x, "radius")

def topdia(x):
  """
  Return the top diameter [mm] (=radius*2000)
  """
  return Feature(x, "TopDia")

def rad(x) :#en mm!
  """
  Return the radius [mm]
  """
  return topdia(x)/2.0

def la(x) :
  """
    Returns the leaf_area value when exists, None/Undef otherwise
  """
  return Feature(x, "leaf_area")

def length(x):
  """
  Return the length [m]
  """
  return Feature(x, "length")
 
def xx(x):
  """
  Return the X position [m]
  """
  return Feature(x, "XX")

def yy(x):
  """
  Return the Y position [m]
  """
  return Feature(x, "YY")

def zz(x):
  """
  Return the Z position [m]
  """
  return Feature(x, "ZZ")


#*************

def uc(p) :
  """
    Returns all components of elmt p that are with Scale=2, i.e. growth unit
  """
  return Components(p, Scale=2)
  
def class_uc(x):
  """
    Transform class of x from G to 1, I to 2 and everything else to 0
  """
  if Class(x) == "G" :
      return 1
  else :
    if Class(x) == "I" :
      return 2
    else :
      return 0

def metamer(p):
  """
    Returns all scale 3 components of p, i.e. all metamers of p
  """
  return Components(p, Scale=3)

def uc1_leafy(p):
  """
  Returns GUs with growing leaves, actually with leaf on the first metamer growing,
  except for bourse shoot
  """
  return [x for x in uc(p) if la(Components(x)[0]) > 0.0 and Class(Father(x))!='I']

def rameaux(p):
  """
  Returns the Fruiting Units, i.e. shoots bearing leafy shoots and fruits
  """
  return list(set([Father(x) for x in uc1_leafy(p) if Father(x) != None]))

def type_uc(x):
  """
  Return the shoot category of UC, i.e. small, medium or large 
  """
  return Feature(metamer(x)[0], 'observation')

def nb_leafy_rameau_cat(x, cat):
  """
  Return the number of leafy shoots of category `cat` of a FU
  Note that bourse counts as 1 small leafy shoot
  """
  nb = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        nb +=1
      try:
        if type_uc(Sons(y)[0]) == cat:
          nb +=1
      except IndexError:
        continue
    elif type_uc(y) == cat:
      nb += 1
  return nb

def nb_leafy_rameau(x):
  """
  Return the total number of leafy shoots of a FU
  Note that bourse counts as 1 small leafy shoot
  """
  return sum([nb_leafy_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

def fruit_nb(x):
  """
  Return the number of fruits on a GU
  """
  return len([y for y in metamer(x) if Feature(y, 'fruit')])

def fruit_ms(x):
  """
  Return the dry weight of fruits on a GU
  """
  return sum([Feature(y, 'fruit') for y in metamer(x) if Feature(y, 'fruit')])

def fruit_ram(x):
  """
  Return the total number of fruits on a FU
  """
  return sum([fruit_nb(y) for y in Sons(x)])

def fruit_ram_ms(x):
  """
  Return the total dry weight of fruits on a FU
  """
  return sum([fruit_ms(y) for y in Sons(x)])

def la_uc(x):
  """
  Returns the total leaf area of given GU
  """
  return sum([la(y) for y in metamer(x)])

def la_rameau_cat(x, cat):
  """
  Return the cumulated leaf area of all leafy shoots of category `cat` of a FU
  """
  la = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        la += la_uc(y)
      try:
        if type_uc(Sons(y)[0]) == cat:
          la += la_uc(Sons(y)[0])
      except IndexError:
        continue
    elif type_uc(y) == cat:
      la += la_uc(y)
  return la

def la_rameaux(x):
  """
  Return the cumulated length of all shoots of a FU
  """  
  return sum([la_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

def length_uc(x):
  """
  Return the length of a GU
  """
  return sum(length(m) for m in metamer(x))

def length_rameau_cat(x, cat):
  """
  Return the cumulated length of all leafy shoots of category `cat` of a FU
  """
  length = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        length += length_uc(y)
      try:
        if type_uc(Sons(y)[0]) == cat:
          length += length_uc(Sons(y)[0])
      except IndexError:
        continue
    elif type_uc(y) == cat:
      length += length_uc(y)
  return length

def lencumul_ram(x):
  """
  Return the cumulated length of all shoots of a FU
  """  
  return sum([length_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

def vol(x):
  """
  Return the volume of the metamer x
  """
  return pi*(topdia(x)/2000.)**2 * length (x)


def vol_uc(x):
  """
  Return the volume of a GU
  """
  return sum([vol(m) for m in metamer(x)])

def vol_pousse(x):
  """
  Return the volume of a shoot, i.e. in case of bourse it returns the 
  cumulated volume of the shoot and all the bourse shoots
  """
  if Class(x) =="I" and Sons(x) != []:
    return vol_uc(x) + sum([vol_uc(y) for y in Sons(x)])
  else:
    return vol_uc(x)	

def vol_rameau_cat(x, cat):
  """
  Return the cumulated volume of all leafy shoots of category `cat` of a FU
  """
  vol = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        vol += vol_uc(y)
      try:
        if type_uc(Sons(y)[0]) == cat:
          vol += vol_uc(Sons(y)[0])
      except IndexError:
        continue
    elif type_uc(y) == cat:
      vol += vol_uc(y)
  return vol


def vol_rameaux(x):
  """
  Return the cumulated volume of all shoots of a FU
  """  
  return sum([vol_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

#===========================================================#
# Utils functions to explore and extract data from 3D scene #
#===========================================================#

def getLeavesOnly(scene, leafcolor="Color_15"):
  return pgl.Scene([ sh for sh in scene if sh.appearance.getName() == leafcolor])

def computeBoundingShape(scene, shape='ellipsoid'):
  """
  Compute a bounding volume for the given `scene`.
  The `shape` of this volume can be one of these keyword 
  Note that the `pgl.fit` could deliver different shapes by using
  one of the following keyword instead of 'ellipsoid':
  EXTRUDEDHULL ; ASYMMETRICHULL ; EXTRUSION ; SPHERE ; ASPHERE ; BSPHERE
  CYLINDER ; ACYLINDER ; BCYLINDER ; ELLIPSOID ; BELLIPSOID2 ; AELLIPSOID
  BELLIPSOID ; AALIGNEDBOX ; BALIGNEDBOX ; BOX ; ABOX ; BBOX ; CONVEXHULL
  """
  
  gr= pgl.Group([ sh.geometry for sh in scene ])
  tglset = pgl.fit( shape, gr )
  #hull = pgl.Shape( tglSet, __Green )
  return tglset

def ellipseDesc(lps):
  """
  Function to extract the center, radii and rotations of a given ellipse
  A bounding ellipse is generated as a Translated(Rotated(Scaled(Sphere)))
  Hence the ellipse center is given by the translation and its radii by the scaling
  """
  unit = 100 #units in QualiTree are in [mm], hence Pgl is in [dm] ?

  if isinstance(lps, pgl.Translated):
    cx, cy, cz = lps.translation
  else:
    print"missing Translated from the bounding ellipse as a Translated(Rotated(Scaled(Sphere)))"

  ori = lps.geometry

  if isinstance(ori, pgl.Oriented):
    rotMat = ori.transformation().getMatrix3()
    az, el, roll = rotMat.eulerAnglesZYX()
  else:
    print"missing Oriented from the bounding ellipse as a Translated(Rotated(Scaled(Sphere)))"
    az = 0
  
  scal = ori.geometry

  if isinstance(scal, pgl.Scaled):
    scMat = scal.transformation().getMatrix()
    rx, ry, rz, rt = scMat.getDiagonal()
  else:
    print"missing Scaled from the bounding ellipse as a Translated(Rotated(Scaled(Sphere)))"
    rx=ry=rz=1

  #x1, y1, z1 #Conversion rep�re MappleT (m) � repr�re Qualitree (q) : Xq=Xm Yq=Zm Zq=-Ym. 
  #Due to change of coordinate axis, rotation needs - pi  <-- apparently not !
  #return cx*unit, cz*unit, -cy*unit, rx*unit, rz*unit, ry*unit, az-3.1415927

  return cx*unit, cz*unit, -cy*unit, rx*unit, rz*unit, ry*unit, az

#===========================================================#

def quote_str(v):
    if type(v) == type(""):
        return "'"+v+"'"
    else:
        return str(v)

def insert_into(table, header, dict_list):
    """
        Renvoie une ligne de commande SQL "INSERT INTO"
        table (string) : la table sur laquelle faire l'insert
        dict_list (list of dict) : en clef le nom des champs de la table, en valeur leur valeur (si on insert une seule ligne) ou un tableau de valeurs (si on insert plusieurs lignes en une commande)
    """
    values = ["(" + ",".join([quote_str(dict[key]) for key in header]) + ")" for dict in dict_list]
    return "INSERT INTO " + table + " ("+",".join(header)+") VALUES\n"+",\n".join(values)+";\n"

def save_csv(header,dict_list,filename):
    values = [";".join([str(dict[key]) for key in header]) for dict in dict_list]
    f=open(filename,'w')
    f.write(";".join(header)+"\n"+"\n".join(values))
    f.close()

def qualitree_nom_rameaux(rmx):
    """ D�fini le nom des rameaux qualitree
    rmx (list of vtx) : liste des rameaux mixtes et du vieux bois.
    Renvoie un dictionaire avec comme clef l'id du vtx et comme valeur le nom Qualitree"""
    
    chiffres = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    fathers = [Father(x) for x in rmx]
    qnames = {rmx[fathers.index(None)]:'r0'}#le tronc n'a pas de p�re.
    rmx2 = [rmx[fathers.index(None)]] #rameaux dont on a d�termin� le nom qualitree mais pas celui de ses enfants
    while len(rmx2) > 0:
        vtx = rmx2[0]#le rameau sur lequel on travaille
        childrens = [rmx[i] for i,x in enumerate(fathers) if x == vtx]#On r�cup�re tous les enfants pr�sents dans rmx (les autres enfants comme les pousses feuill�es sont exclus)
        
        rmx2 = rmx2[1:]#On retire le rameau de la liste des rameaux dont il faut d�terminer le nom des enfants
        rmx2 += childrens #On rajoutte les enfants dans la liste
        
        if len(childrens)>0:#Si le rameau a des enfants on les nomme
            vtx_metamers = Components(vtx)
            childrens_metamer_position = [vtx_metamers.index(Father(Components(x)[0])) for x in childrens]#position du p�re des enfants dans vtx (� l'�chelle du m�tam�re)
            sorted_metamer_position = sorted(childrens_metamer_position)
            childrens_position = [sorted_metamer_position.index(x)+1 for x in childrens_metamer_position] #position des enfants entre eux (1 pour le premier, 2 pour le deuxi�me...).
            
            c_p=[]
            for i in childrens_position:#Si il y a des doublons dans childrens_position on incr�mente l'un d'entre eux (quand eux rameaux partent du m�me m�tam�re)
                if i not in c_p:
                    c_p.append(i)
                else:
                    c_p.append(i+1)
            childrens_position=c_p

            if qnames[vtx]=='r0':#les fils du tronc sont nomm�es r1, r2, r3...
                for k in range(len(childrens)):
                    assert childrens_position[k] <= len(chiffres), 'Le rameau r0 a {rams} ramifications, ce qui est sup�rieur au nombre maximal de {max}'.format(rams=childrens_position[k],max=len(chiffres))
                    qnames[childrens[k]]='r'+str(chiffres[childrens_position[k]-1])
            else:#sinon ils ont le nom du p�re suivi de -0, -1, -2...
                for k in range(len(childrens)):
                    qnames[childrens[k]]=qnames[vtx]+'-'+str(chiffres[childrens_position[k]-1])

    return qnames


def niveau(name):
    return 0 if name == 'r0' else name.count('-')+1


def qualitree_metamer(rmx, names):
  """
  Il faut renseigner la "longeur du m�tam�re" pour chaque rameau dans la base de donn�es.
  Cette valeur est la longeur en mm entre la ramification pr�c�dente et celle portant le rameau,
  sur le rameau parent.
  """
  metameres_qualitree = {}
  chiffres = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  for x in rmx:
    if(Father(x)==None):#La "longueur du m�tam�re" n'a pas de sens pour le tronc.
      metameres_qualitree[x] = 0#Qualitree demande que l'on indique 0.
    else:
      intervale = None
      father_mets = Components(Father(x)) #m�tam�res du du p�re de x
      ramif_index = father_mets.index(Father(Components(x)[0])) #position du m�tam�re (au sens de MAppleT) portant le rameau x sur le p�re de x.
      if names[x][-1]=="1":#Pour la premi�re ramification d'un rameau, le m�tam�re est sa distance avec le d�but du parent.
        intervale = father_mets[:ramif_index+1] #Liste des m�tam�res dont la longueur doit etre compt�e.
      else:#Pour les ramifications suivantes, on prends la longeur entre cette ramification et la pr�c�dente.
        nom_ramif_prec = names[x][:-1] + chiffres[chiffres.index(names[x][-1])-1]
        ramif_prec = [c for c,v in names.items() if v == nom_ramif_prec][0]
        index_ramif_prec = father_mets.index(Father(Components(ramif_prec)[0]))
        intervale = father_mets[index_ramif_prec+1:ramif_index+1]

      met = round(sum([length(m) for m in intervale])*1000,1)
      metameres_qualitree[x] = met if met != 0 else 1

  return metameres_qualitree

#===========================================================#

def tree_sql(save_pth, nom_arbre, date, arbre, architecture,rameauxmixte, ellipseIN=False):
    """
        G�n�re le code sql permettant de supprimer un arbre dans la base de donn�e de qualitree
        Renvoie la requ�te SQL en string
        nom_arbre (str) : nom de l'arbre dans la base de donn�es qualitree
        date (str) : date � laquelle l'arbre � �t� mesur� sous la forme YYYY-MM-DD
        variete (str) : vari�t�
        vr_masse_seche (float) : masse s�che des vielles racines (grammes)
        jr_masse_seche (float) : masse s�che des jeunes racines (grammes)
        vb_masse_seche (float) : masse s�che du vieux bois (grammes)
        architecture (list of list) : liste de listes repr�sentant les rameaux mixtes et le vieux bois sous la forme : niveau (int), nom_rameau (str), diametre_base, diametre_ext, metamere, x1, y1, z1, x2, y2, Z2
        rameauxmixte (list of list) : liste de listes repr�sentant les rameaux mixtes sous la forme : nom_rameau, tl_masse_seche, f2_nombre_unites, f2_masse_seche, pfx_nombre_unites, pfx_masse_seche
        ellipseIN
     """

    #Si il y a un arbre du m�me nom et ann�e, on le supprime.
    sql = "DELETE FROM arbre WHERE nom_arbre='"+nom_arbre+"';\n"
    sql+= "DELETE FROM architecture WHERE nom_arbre='"+nom_arbre+"';\n"
    sql+= "DELETE FROM rameauxmixte WHERE nom_arbre='"+nom_arbre+"';\n"

    #table "arbre"
    if ellipseIN:
      header = ['nom_arbre', 'date', 'variete', 'vr_masse_seche', 'jr_masse_seche', 'vb_masse_seche', 'ci_x', 'ci_y', 'ci_z', 'ri_x', 'ri_y', 'ri_z', 'coupe_h', 'coupe_b', 'angle_y']
      ins_arbre = [{'nom_arbre':nom_arbre, 'date':date, 'variete':arbre[0], 'vr_masse_seche':arbre[1], 'jr_masse_seche':arbre[2], 'vb_masse_seche':arbre[3], 'ci_x':arbre[4], 'ci_y':arbre[5], 'ci_z':arbre[6], 'ri_x':arbre[7], 'ri_y':arbre[8], 'ri_z':arbre[9], 'coupe_h':arbre[10], 'coupe_b':arbre[11], 'angle_y':arbre[12]}]
    else:
      header = ['nom_arbre', 'date', 'variete', 'vr_masse_seche', 'jr_masse_seche', 'vb_masse_seche']
      ins_arbre = [{'nom_arbre':nom_arbre, 'date':date, 'variete':arbre[0], 'vr_masse_seche':arbre[1], 'jr_masse_seche':arbre[2], 'vb_masse_seche':arbre[3]}]


    sql += insert_into('arbre', header, ins_arbre)
    #sql+= insert_into("arbre",header,[{'nom_arbre':nom_arbre, 'date':date, 'variete':variete, 'vr_masse_seche':vr_masse_seche, 'jr_masse_seche':jr_masse_seche, 'vb_masse_seche':vb_masse_seche}])

    #table "architecture" (g�om�trie rammeaux mixte + vieux bois)
    header = ['nom_arbre','niveau', 'nom_rameau', 'annee', 'diametre_base', 'diametre_ext', 'metamere', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'longueur']
    ins_architecture = [{'nom_arbre':nom_arbre,'niveau':rameau[0], 'nom_rameau':rameau[1], 'annee':int(date.split("-")[0]), 'diametre_base': rameau[2], 'diametre_ext' : rameau[3], 'metamere' : rameau[4], 'x1' :rameau[5], 'y1':rameau[6], 'z1':rameau[7], 'x2':rameau[8], 'y2':rameau[9], 'z2':rameau[10], 'longueur':rameau[11]} for rameau in architecture]
    sql+= insert_into("architecture",header,ins_architecture)
    
    #table "rameauxmixte" (mati�re s�che, concentration en sucres, nombre de pousses feuill�es et de fruits...).
    header = ['nom_arbre', 'nom_rameau', 'date', 'tl_masse_seche', 'f2_tms_pulpe','f2_concent_sorbitol', 'f2_concent_sucrose', 'f2_concent_glucose', 'f2_concent_fructose', 'f2_nombre_unites', 'f2_masse_seche', 'pf1_nombre_unites', 'pf1_masse_seche', 'pf2_nombre_unites', 'pf2_masse_seche', 'pf3_nombre_unites', 'pf3_masse_seche']
    valeurs_sucres = (0.0018, 0.0104, 0.0185, 0.0182)#Valeurs "bidon" de teneur en sucre des fruits (n�cessaire pour le mod�le mais n'existe pas chez le pommier). Les valeurs prises sont celles de la vari�t� alexandra.
    ins_ram = [{'nom_arbre': nom_arbre , 'nom_rameau': rameau[0]  , 'date': date , 'tl_masse_seche': rameau[1], 'f2_concent_sorbitol': valeurs_sucres[0] , 'f2_concent_sucrose': valeurs_sucres[1] , 'f2_concent_glucose': valeurs_sucres[2] , 'f2_concent_fructose': valeurs_sucres[3] , 'f2_nombre_unites': rameau[2] , 'f2_masse_seche': rameau[3] , 'pf1_nombre_unites': rameau[4] , 'pf1_masse_seche': rameau[5], 'pf2_nombre_unites': rameau[6] , 'pf2_masse_seche': rameau[7], 'pf3_nombre_unites': rameau[8] , 'pf3_masse_seche': rameau[9], 'f2_tms_pulpe': rameau[11]}for rameau in rameauxmixte]
    sql += insert_into("rameauxmixte",header,ins_ram)
    f = open(op.join(save_pth, str(nom_arbre)+'_'+str(date)+'.sql'), 'w')
    f.write(sql)
    f.close()

    #return sql


def tree_csv(save_pth, nom_arbre, date, variete, vr_masse_seche, jr_masse_seche, vb_masse_seche, architecture,rameauxmixte):
    #table "architecture" (g�om�trie rammeaux mixte + vieux bois)
    header = ['index','nom_arbre','niveau', 'nom_rameau', 'annee', 'diametre_base', 'diametre_ext', 'metamere', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'longueur']
    ins_architecture = [{'index': rameau[12],'nom_arbre':nom_arbre,'niveau':rameau[0], 'nom_rameau':rameau[1], 'annee':int(date.split("-")[0]), 'diametre_base': rameau[2], 'diametre_ext' : rameau[3], 'metamere' : rameau[4], 'x1' :rameau[5], 'y1':rameau[6], 'z1':rameau[7], 'x2':rameau[8], 'y2':rameau[9], 'z2':rameau[10], 'longueur':rameau[11]} for rameau in architecture]
    save_csv(header, ins_architecture, op.join(save_pth, str(nom_arbre) + '_' + str(date) + "_architecture.csv"))
    
    #table "rameauxmixte" (mati�re s�che, concentration en sucres, nombre de pousses feuill�es et de fruits...).
    header = ['index','nom_arbre', 'nom_rameau', 'date', 'tl_masse_seche', 'f2_tms_pulpe', 'f2_concent_sorbitol', 'f2_concent_sucrose', 'f2_concent_glucose', 'f2_concent_fructose', 'f2_nombre_unites', 'f2_masse_seche', 'pf1_nombre_unites', 'pf1_masse_seche', 'pf2_nombre_unites', 'pf2_masse_seche', 'pf3_nombre_unites', 'pf3_masse_seche']
    valeurs_sucres = (0.0018, 0.0104, 0.0185, 0.0182)#Valeurs "bidon" de teneur en sucre des fruits (n�cessaire pour le mod�le mais n'existe pas chez le pommier). Les valeurs prises sont celles de la vari�t� alexandra.
    ins_ram = [{'index': rameau[10],'nom_arbre': nom_arbre , 'nom_rameau': rameau[0]  , 'date': date , 'tl_masse_seche': rameau[1], 'f2_concent_sorbitol': valeurs_sucres[0] , 'f2_concent_sucrose': valeurs_sucres[1] , 'f2_concent_glucose': valeurs_sucres[2] , 'f2_concent_fructose': valeurs_sucres[3] , 'f2_nombre_unites': rameau[2] , 'f2_masse_seche': rameau[3], 'pf1_nombre_unites': rameau[4] , 'pf1_masse_seche': rameau[5], 'pf2_nombre_unites': rameau[6] , 'pf2_masse_seche': rameau[7], 'pf3_nombre_unites': rameau[8] , 'pf3_masse_seche': rameau[9], 'f2_tms_pulpe': rameau[11]} for rameau in rameauxmixte]
    save_csv(header, ins_ram, op.join(save_pth, str(nom_arbre) + '_' + str(date) + "_rameauxmixtes.csv"))

#===========================================================#

def export2qualitree(save_pth, mtg_file_path, leaf_scene, nom_arbre,date,variete,SLA,densite_MS_rameaux,TMS_fruits,SR,userEllipse=True, charge_fruits=None,seed=None, pf_type='default'):
    '''
    Converti un fichier .mtg g�n�r� par MAppleT en une architecure au format Qualitree. Le script .sql est renvoy� en sorti de cette fonction (il faudra l'enregistrer dans un fichier),
    des fichiers .csv correspondants aux tables de la bdd Qualitree sont aussi g�n�r�s (cela permet de visualiser le r�sultat plus facilement qu'en SQL).

    mtg_file : chemin vers le .mtg que l'on souhaite convertir.
    nom_arbre : le nom � donner � l'architecture dans la base de donn�es de qualitree.
    date : date � indiquer dans la base de donn�es de qualitree (date de d�but de simulation)
    variete : vari�t�, tel que not�e dans le fichier parametres.xml
    SLA : specific leaf area
    densite_MS_rameaux : densit� du bois en g.m-3
    TMS_fruits : teneur en mati�re s�che des fruits
    SR : shoot-root ratio utilis� pour calculer la masse des jeunes ou vieilles racines en fonction de celle des pousses feuill�es ou du vieux bois+tiges de rameaux mixtes (respectivement)
    charge_fruits : par d�faut les fruits sont ceux indiqu�s dans le .mtg. Si une valeur est indiqu�e (entre 0. et 1.), elle d�fini la proportion d'inflorescences portant un fruit (0.: pas de fruits, 1.: un fruit par inflorescence).  
    La masse des fruits quand la charge est fix�e est �gale � la moyenne de la masses des fruits dans le .mtg
    seed : graine du g�n�rateur de nombre pseudo al�atoire utilis� pour d�terminer quelles inflorescences portent un fruit, par d�faut la graine est al�atoire.
    '''

    #Open the MTG file, only the first plant/tree will be considered in case of multiple plants in the same file
    m = MTG(mtg_file_path)
    plants = VtxList(Scale=1)
    
    #Get the ordered list of GU year of appearance, fruiting unit are the before last-year ones
    annees = sorted(list(set([an(x) for x in uc(plants[0])])))

    ram_mixtes = rameaux(plants[0]) #rameaux mixtes

    #Les rameaux mixtes doivent �tre des UC de l'ann�e pr�c�dente, sinon la condition de qualitree comme quoi un rameau mixte ne peut pas porter de ramifications n'est pas respect�e, hors des bugs de MAppleT peuvent entrainer que certaines feuilles ne tombent pas ou que plusieurs UC soient produites dans la m�me ann�e, les rameaux non conformes sont supprim�s. 
    for r in [x for x in ram_mixtes if an(x) != annees[-2]]:
        print 'ERREUR : rameaux mixte ' + Class(r) + str(Index(r)) +  ' avec pour ann�e de croissance ' + str(an(r)) + '. Ce rameau ne sera pas consid�r� comme mixte'
        
    ram_mixtes = [x for x in ram_mixtes if an(x) == annees[-2]]

    #Getting all the branches, i.e fruiting units + old wood
    rm = ram_mixtes
    while True:
        rm_new = list(set([Father(x) for x in rm] + rm))#On ajoutte le vieux bois
        if len(rm_new) == len(rm):#On s'arr�te quand on ne trouve plus de nouveaux rameaux.
            break
        else:
            rm = rm_new
    rm = [x for x in rm if  x != None]

    #Generate the GU names according to QualiTree naming convention
    names = qualitree_nom_rameaux(rm)

    #Getting the QualiTree metamer info, i.e. length between the current GU and the previous one on the bearing shoot
    metameres_qualitree = qualitree_metamer(rm, names)

    #=====================================#
    # Generate info for architecture table#
    #=====================================#


    #QualiTree does not allow shoot positions to be below ground whereas it may results from MAppleT bending
    base_sous_sol = [x for x in rm if zz(Components(x)[0]) <= 0]
    sommet_sous_sol = [x for x in rm if zz(Components(x)[-1]) <= 0]
    for r in base_sous_sol:
        print 'ERREUR : la base de l\'UC ' + Class(r) + str(Index(r)) + ' est sous le plan horizontal, Y1 sera fix� � 0.1'
    for r in sommet_sous_sol:
        print 'ERREUR : le sommet de l\'UC ' + Class(r) + str(Index(r)) + ' est sous le plan horizontal, Y2 sera fix� � 0.1'

    tab_architecture = [[
             niveau(names[x]),#Order(x),#marche pas?
             names[x],
             topdia(Components(x)[0]),#diametre_base
             topdia(Components(x)[-1]),#diametre_ext
             metameres_qualitree[x],#metameres
             round(xx(Components(x)[0])*1000,1),round((zz(Components(x)[0]) if (zz(Components(x)[0]) > 0.0) else 0.0001)*1000,1),round(-yy(Components(x)[0])*1000,1),#x1, y1, z1 #Conversion rep�re MappleT (m) � repr�re Qualitree (q) : Xq=Xm Yq=Zm Zq=-Ym, conversion m -> mm. On s'assure que Y > 0 sinon on le fixe � 0 (condition qualitree).
             round(xx(Components(x)[-1])*1000,1),round((zz(Components(x)[-1]) if zz(Components(x)[-1]) > 0.0 else 0.0001)*1000,1),round(-yy(Components(x)[-1])*1000,1),
             round(length_uc(x)*1000,1),
             Class(x) + str(Index(x)),
            ]for x in rm]
    #save(tab_architecture,'test.csv')

    #=====================================#
    # Generate info for rameauxmixte table#
    #=====================================#

    ### Charge option
    if charge_fruits == None:        
        fruit_nb = fruit_ram
        fruit_dw = fruit_ram_ms

    else:
        charge_fruits = float(charge_fruits)
        assert(0. <= charge_fruits and charge_fruits <= 1.)
        if seed != None:
            random.seed(seed)
        ms_moy_fruit = float(sum([fruit_ram_ms(x) for x in ram_mixtes]))/sum([fruit_ram(x) for x in ram_mixtes])
        nb_I =  [len([y for y in Sons(x) if Class(y) == "I"]) for x in ram_mixtes]
        nb_F = int(round(sum(nb_I) * charge_fruits))

        inflos = []
        for x,i in zip(ram_mixtes,nb_I):
            inflos += [x]*i
        random.shuffle(inflos)
        inflos = inflos[0:nb_F]#On choisi au hasard les inflorescences portant un fruit.
        ram_mixte_nb_F = {x:inflos.count(x) for x in ram_mixtes} 

        fruit_nb = lambda x:ram_mixte_nb_F[x]
        fruit_dw = lambda x:ram_mixte_nb_F[x]*ms_moy_fruit

    ### Option leafy_shoot type
    small_nb = lambda x: nb_leafy_rameau_cat(x, 'small')
    small_dw = lambda x: la_rameau_cat(x, 'small')/SLA + vol_rameau_cat(x, 'small')*densite_MS_rameaux
    medium_nb = lambda x: nb_leafy_rameau_cat(x, 'medium')
    medium_dw = lambda x: la_rameau_cat(x, 'medium')/SLA + vol_rameau_cat(x, 'medium')*densite_MS_rameaux
    large_nb = lambda x: nb_leafy_rameau_cat(x, 'large')
    large_dw = lambda x: la_rameau_cat(x, 'large')/SLA + vol_rameau_cat(x, 'large')*densite_MS_rameaux


    if pf_type == 'all1':
      pf1_nb = lambda x: small_nb(x) + medium_nb(x) + large_nb(x)
      pf1_dw = lambda x: small_dw(x) + medium_dw(x) + large_dw(x)
      pf2_nb = lambda x: 0
      pf2_dw = lambda x: 0
      pf3_nb = lambda x: 0
      pf3_dw = lambda x: 0
    elif pf_type == 'all2':
      pf1_nb = lambda x: 0
      pf1_dw = lambda x: 0
      pf2_nb = lambda x: small_nb(x) + medium_nb(x) + large_nb(x)
      pf2_dw = lambda x: small_dw(x) + medium_dw(x) + large_dw(x)
      pf3_nb = lambda x: 0
      pf3_dw = lambda x: 0
    elif pf_type == 'all3':
      pf1_nb = lambda x: 0
      pf1_dw = lambda x: 0
      pf2_nb = lambda x: 0
      pf2_dw = lambda x: 0
      pf3_nb = lambda x: small_nb(x) + medium_nb(x) + large_nb(x)
      pf3_dw = lambda x: small_dw(x) + medium_dw(x) + large_dw(x)
    else:
      pf1_nb = small_nb
      pf1_dw = small_dw
      pf2_nb = medium_nb
      pf2_dw = medium_dw
      pf3_nb = large_nb
      pf3_dw = large_dw
      # dry weight is the sum of leaves dw woody part dw

    ### Generate Rameaux mixte table

    tab_rameauxmixte = [[names[x],
                       vol_uc(x)*densite_MS_rameaux,
                       fruit_nb(x),
                       fruit_dw(x),
                       pf1_nb(x),
                       pf1_dw(x),
                       pf2_nb(x),
                       pf2_dw(x),
                       pf3_nb(x),
                       pf3_dw(x),
                       Index(x),
                       TMS_fruits,
                       ] for x in ram_mixtes]
 
    """
    tab_rameauxmixte = [[names[x],
                       vol_uc(x)*densite_MS_rameaux,
                       fruit_nb(x),
                       fruit_dw(x),
                       nb_leafy_rameau_cat(x, 'small'),
                       la_rameau_cat(x, 'small')/SLA + vol_rameau_cat(x, 'small')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuill�es
                       nb_leafy_rameau_cat(x, 'medium'),
                       la_rameau_cat(x, 'medium')/SLA + vol_rameau_cat(x, 'medium')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuill�es
                       nb_leafy_rameau_cat(x, 'large'),
                       la_rameau_cat(x, 'large')/SLA + vol_rameau_cat(x, 'large')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuill�es
                       Index(x),
                       TMS_fruits,
                       ] for x in ram_mixtes]
    """
    #save(tab_rameauxmixte,'test2.csv')


    #=====================================#
    #   Generate info for arbre table     #
    #=====================================#
    vb_masse_seche = sum([vol_uc(x)*densite_MS_rameaux for x in rm if not x in ram_mixtes])
    vb_masse_seche = vb_masse_seche if vb_masse_seche != None else 0#Pour les arbres jeunes (sans vieux bois), sum([]) = None
    vr_masse_seche = sum([vol_uc(x)*densite_MS_rameaux for x in rm])/SR #La masse s�che de vieilles racines est calcul�e en fonction de la masse des UC en croissance secondaire (vieux bois+tiges de rameaux mixte) et du shoot-root ratio.
    jr_masse_seche = sum([la_rameaux(x)/SLA + sum([vol_uc(y) for y in Sons(x)])*densite_MS_rameaux for x in ram_mixtes])/SR #La masse s�che des jeunes racines est calcul�e en fonction de la masse des pousses feuill�es (tige+feuilles) et du shoot-root ratio.

    #delete MTG in memory
    del m


    if userEllipse:
      #To get an estimation of the ellipse we use PlantGL algorithms, hence the need of the 3D scene
      #The scene should be a pgl.Scene but could also be the path to a saved bgeom scene
      if type(leaf_scene) == str:
        sc = pgl.Scene(leaf_scene)
      else:
        sc = leaf_scene

      assert type(sc) == pgl.Scene

      #The scene should only contains the leaves
      #in MAppleT it can be obtained using their specific colorname 
      #lvs = getLeavesOnly(sc)

      #Computing the ellipse
      #ell = computeBoundingShape(lvs)
      ell = computeBoundingShape(sc)

      #Retrieving the info of that ellipse
      cx,cy,cz,rx,ry,rz,angle_y = ellipseDesc(ell)
      #For the moment the high and low cutting planes are defined at the top and bottom of the ellipse
      coupe_h = cy+ry
      #coupe_b = cy-ry
      #trying to use the leaves BBox to define the low cutting plane
      bbox = pgl.BoundingBox(sc)
      coupe_b = bbox.getZMin()*100
      

      tab_arbre = [variete,vr_masse_seche, jr_masse_seche, vb_masse_seche, cx, cy, cz, rx, ry, rz, coupe_h, coupe_b, angle_y]
      tree_sql(save_pth, nom_arbre,date,tab_arbre,tab_architecture,tab_rameauxmixte, ellipseIN=True)
    else:
      tab_arbre = [variete,vr_masse_seche, jr_masse_seche, vb_masse_seche]
      tree_sql(save_pth, nom_arbre,date,tab_arbre,tab_architecture,tab_rameauxmixte, ellipseIN=False)


    tree_csv(save_pth, nom_arbre,date,variete,vr_masse_seche, jr_masse_seche, vb_masse_seche,tab_architecture,tab_rameauxmixte)
    #return tree_sql(nom_arbre,date,tab_arbre,tab_architecture,tab_rameauxmixte)

