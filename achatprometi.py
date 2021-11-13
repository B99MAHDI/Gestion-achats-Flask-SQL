from flask import Flask, render_template, request, redirect, url_for , session , flash, send_file
from functools import wraps
import os
import mysql.connector
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import math
import os
from io import BytesIO


app = Flask(__name__)
app.secret_key =os.urandom(20)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=3600 * 24)
#connection  = mysql.connector.connect(host='B99MAHDI.mysql.pythonanywhere-services.com',user='B99MAHDI',password='achatprometi_db_2021', database='achatprometi')
connection  = mysql.connector.connect(user='root',password='', database='achatprometi')
mycursor = connection.cursor()
mycursor1 = connection.cursor()
mycursor2 = connection.cursor()
mycursor.execute("SELECT * FROM `info_tousarticles`")
data2 = mycursor.fetchall()

#FLASK_ENV='development'

@app.errorhandler(401)
def unauthorized():
    return "<h1 style='text-align:center;'>Vous n'étes pas autorisé à cette page !! :(</h1>", 401


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logged_in'))
    return wrap


@app.route('/')
def Home():
    return render_template('Achat_PROMETI_HOME.html')


@app.route('/9182<int:id>7456/<string:name>/parametrage_app', methods=['GET','POST'])
@login_required
def parametrage(id,name):
    try:
        if request.method == 'GET':
            mycursor.execute("SELECT * FROM `parametres_app` WHERE `Id`=%s",(id,))
            prm_data = mycursor.fetchall()
            prm = prm_data[0]
            nom=prm[3]
            desc=prm[4]
            app_email=prm[6]
            adress=prm[5]
            secret_key = prm[2]
            name=name
            return render_template("parametrage.html",nom=nom,desc=desc,app_email=app_email,adress=adress,secret_key=secret_key)        
    except:
        return unauthorized()    


@app.route('/9182<int:id>7456/<string:name>/parametrage_app/update', methods=['GET','POST'])
@login_required
def parametrage_up(id,name):
    try:
        if request.method == 'POST':
            nom = request.form['nom']
            desc = request.form['desc']
            app_email = request.form['app_email']
            adress = request.form['adress']
            secret_key = request.form['secret_key']
            mycursor.execute("UPDATE `parametres_app` SET `nom_app`=%s , `desc_app`=%s , `email_app`=%s , `addr_app`=%s , `secret_app`=%s ",(nom,desc,app_email,adress,secret_key,))
            return redirect(url_for('parametrage' , id=id,name=name))
    except:
        return unauthorized()  


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


@app.route('/9182<int:id>7456/<string:name>/download/<string:Nom>',methods=['GET','POST'])
@login_required
def toexcel(id,name,Nom):
    try:
        id=id
        name=name
        liste = []
        mycursor.execute("SELECT * FROM `tous_articles` WHERE Nom_table=%s",(Nom,))
        data_imprimer = mycursor.fetchall()
        for row in data_imprimer:
            data_row = [row[2],row[3],row[4]]
            liste.append(data_row)
        df_imprimer = pd.DataFrame(liste, columns=['Client', 'Désignation', 'Prix Unitaire'])
        df_imprimer.to_excel("Base_de_données_("+Nom+").xlsx", sheet_name=Nom,index=False)
        excel_file = convertToBinaryData("Base_de_données_("+Nom+").xlsx")
        mycursor1.execute("UPDATE `info_tousarticles` SET `enregistrement`=%s WHERE Nom_table="+Nom+";",(excel_file,))
        mycursor2.execute("SELECT `enregistrement` FROM `info_tousarticles` WHERE Nom_table="+Nom+";")
        file = mycursor2.fetchall()
        file_tuple = file[0]
        connection.commit()
    except :
        return "<h1 style='text-align:center;'>page not found.</h1>"
    finally:
        connection.close()
        return send_file(BytesIO(file_tuple[0]), attachment_filename="Base de données ("+Nom+").xlsx" , as_attachment=True)


@app.route('/9182<int:id>7456/<string:name>/download/tous_articles',methods=['GET','POST'])
@login_required
def allarticles_toexcel(id,name):
    try:
        id=id
        name=name
        liste = []
        mycursor.execute("SELECT * FROM tous_articles")
        data_imprimer = mycursor.fetchall()
        for row in data_imprimer:
            data_row = [row[1],row[2],row[3],row[4]]
            liste.append(data_row)
        df_imprimer = pd.DataFrame(liste, columns=['Nom de la table','Client', 'Désignation', 'Prix Unitaire'])
        df_imprimer.to_excel('tous_les_articles.xlsx', sheet_name='tous_les_articles',index=True)
        excel_file = convertToBinaryData("tous_les_articles.xlsx")
        mycursor1.execute("UPDATE `enregistrement_xlsx` SET `enregistrement`=%s WHERE Nom_table='tous_articles';",(excel_file,))
        mycursor2.execute("SELECT `enregistrement` FROM `enregistrement_xlsx` WHERE Nom_table='tous_articles'")
        file = mycursor2.fetchall()
        file_tuple = file[0]
        connection.commit()
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"
    finally:
        return send_file(BytesIO(file_tuple[0]), attachment_filename="tous les articles.xlsx" , as_attachment=True)


@app.route('/9182<int:id>7456/<string:name>/download/fournisseurs',methods=['GET','POST'])
@login_required
def suppliers_toexcel(id,name):
    try:
        id=id
        name=name
        liste = []
        mycursor.execute("SELECT * FROM `achat_fournisseur`")
        data_imprimer = mycursor.fetchall()
        for row in data_imprimer:
            data_row = [row[1],row[2],row[3],row[4],row[5],row[6]]
            liste.append(data_row)
        df_imprimer = pd.DataFrame(liste, columns=['CT_Num','DL_Design','Prix Unitaire','Commerciale', 'Numéro du Télèphone', 'Adresse Email'])
        df_imprimer.to_excel('Base_de_données_fournisseurs.xlsx', sheet_name='Achat_Fournisseurs',index=False)
        excel_file = convertToBinaryData("Base_de_données_fournisseurs.xlsx")
        mycursor1.execute("UPDATE `enregistrement_xlsx` SET `enregistrement`=%s WHERE Nom_table='achat_fournisseur';",(excel_file,))
        mycursor2.execute("SELECT `enregistrement` FROM `enregistrement_xlsx` WHERE Nom_table='achat_fournisseur';")
        file = mycursor2.fetchall()
        file_tuple = file[0]
        connection.commit()
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"
    finally:
        connection.close()
        return send_file(BytesIO(file_tuple[0]), attachment_filename="Base de données achat_fournisseur.xlsx" , as_attachment=True)





@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Profile', methods=['GET','POST'])
@login_required
def profile(id,name):
#try:
    #if id in session and name in session:
    id=id
    name=name
    #if request.form.get('compte'):
    #    redirect(url_for('account_up',id,name))
    #else :
    return render_template('Achat_PROMETI_Profile.html',id=id,name=name)
    #else :
        #return "the page that you are looking for is not found."
#except:
#    return "<h1 style='text-align:center;'>page not found.</h1>"




#@app.route("/9182<int:id>7456/<string:name>/compte/update/upload-image", methods=["GET", "POST"])
#def upload_image(id,name):
#    if request.method == "POST":
#        if request.files:
#            image = request.files["image"]
#            mycursor.execute("UPDATE `login` SET Photo=%s WHERE Id=%s",(image,id,))
#            return render_template('compte.html',id=id,name=name)
#    return redirect(url_for('account_up',id=id,name=name))


@app.route('/9182<int:id>7456/<string:name>/compte/update' , methods=['GET','POST'])
@login_required
def account_up(id,name):
    try:
        error = None
        if request.method == 'POST':
            mlname = request.form['nom'] 
            name = request.form['prenom']
            myemail = request.form['email'] 
            mypssd = request.form['mdp'] 
            listpswd = list(mypssd)
            nbpwd = len(listpswd)
            remypssd = request.form['re_mdp']
            if not mlname:
                error = "Vous avez oublié votre Nom. Veuillez entrer à nouveau vos informations."
            elif not name:    
                error = "Vous avez oublié votre Prénom. Veuillez entrer à nouveau vos informations."
            elif not myemail:
                error = "Vous avez oublié votre Email. Veuillez entrer à nouveau vos informations."
            elif not nbpwd :
                error = 'Le Mot de passe est important !! Veuillez entrer à nouveau vos informations.'
            elif nbpwd < 8 or nbpwd == 0 :
                error = 'Le mot de passe que vous avez entré est très court. Veuillez entrer à nouveau vos informations.'
            elif remypssd != mypssd:
                error = 'Les deux mots de passe que vous avez entré sont différents !! Veuillez entrer à nouveau vos informations.'
            else:
                try:
                    hashedpsw = generate_password_hash(mypssd)
                    mycursor.execute("UPDATE `login` SET Nom=%s, Prénom=%s, Email=%s, Password=%s WHERE Id=%s",(mlname,name,myemail,hashedpsw,id))
                    connection.commit()
                    message = "Vos informations sont bien enregistrées. Veuillez quitter cette page sans rien faire."
                    return render_template('compte.html', error=error , id=id , name=name,message=message)
                except:
                    return "<h1 style='text-align:center;'>page not found.</h1>"
        return render_template('compte.html', error=error , id=id , name=name)
    except :
        return "<h1 style='text-align:center;'>page not found.</h1>"

@app.route('/9182<int:id>7456/<string:name>/compte' , methods=['GET','POST'])
@login_required
def account_data(id,name):
    try:
        if request.method=='GET':
            mycursor.execute("SELECT * FROM `login` WHERE `Id`=%s AND `Prénom`=%s",(id,name))
            logdatas = mycursor.fetchall()
            log = logdatas[0]
            mlname=log[1]
            name=log[2]
            myemail=log[3]
            mypssd=log[4]
            return render_template("compte.html",id=id,name=name,mlname=mlname,myemail=myemail,mypssd=mypssd)
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"




@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_DB',methods=['GET','POST'])
@login_required
def artcldb(id,name):
    try:
        return render_template('Achat_PROMETI_Articles_DB.html' ,id=id,name=name, data2=data2)
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route("/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_DB/tous_articles/Page = <int:page>",methods=['GET','POST'])
@login_required
def ttarticle(id,name,page):
    try:
        mycursor2 = connection.cursor()
        mycursor2.execute("SELECT COUNT(*) FROM `tous_articles`")
        tuple_nombre_articles = mycursor2.fetchone()
        nombre_articles = tuple_nombre_articles[0]
        nombre_pages = math.ceil(nombre_articles/500)
        liste = list(range(1,nombre_pages+1))
        pageP = page - 1
        if request.method=='GET':
            try:
                if page <= 0 :
                    return "<h1 style='text-align:center;'>page not found.</h1>"
                elif page > nombre_pages + 1  :
                    return"<h1 style='text-align:center;'>page not found.</h1>"
                else :
                    page2 = 500*pageP
                    mycursor1.execute("SELECT * FROM ((SELECT * FROM `tous_articles`) AS tous_articles_REV) ORDER BY id DESC LIMIT 500 OFFSET "+str(page2)+";")
                    data8 = mycursor1.fetchall()
                    pageS = page + 1
                    Lpage = nombre_pages
                    return render_template('tous_les_articles.html',id=id,name=name,data8=data8,page=page,pageS=pageS,Lpage=Lpage,liste=liste,pageP=pageP,nombre_articles=nombre_articles)
            except:
                return "une Erreur s'est produite. "
        elif request.method=='POST':
            if request.form.get('search'):
                try:
                    word_to_search = request.form['search']
                    mycursor.execute("SELECT * FROM `tous_articles` WHERE (`Nom_table` LIKE '%"+word_to_search+"%') OR (`Client` LIKE '%"+word_to_search+"%') OR (`Désignation` LIKE '%"+word_to_search+"%') OR (`PrixUnitaire` LIKE '%"+word_to_search+"%')")
                    data1 = mycursor.fetchall()
                    connection.commit()
                    return render_template('all_results.html',id=id,name=name,data1=data1)
                except:
                    return "une Erreur s'est produite. "
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"





@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_DB/<string:Nom>/Page = <int:page>',methods=['GET','POST'])
@login_required
def data(id,name,Nom,page):
    try:
        mycursor2 = connection.cursor()
        mycursor2.execute("SELECT COUNT(*) FROM `tous_articles` WHERE Nom_table='"+Nom+"'")
        tuple_nombre_articles = mycursor2.fetchone()
        nombre_articles = tuple_nombre_articles[0]
        nombre_pages = math.ceil(nombre_articles/500)
        liste = list(range(1,nombre_pages+1))
        pageP = page - 1
        if request.method=='GET':
            try:
                if page <= 0 :
                    return "<h1 style='text-align:center;'>page not found.</h1>"
                elif page > nombre_pages + 1 :
                    return"<h1 style='text-align:center;'>page not found.</h1>"
                else :
                    page2 = 500*pageP
                    mycursor.execute("SELECT * FROM ((SELECT * FROM `tous_articles` WHERE Nom_table=%s) AS tous_articles_REV) ORDER BY id DESC LIMIT 500 OFFSET "+str(page2)+";",(Nom,))
                    data = mycursor.fetchall()
                    pageS = page + 1
                    Lpage = nombre_pages
                    return render_template('Article1.html',id=id,name=name,data=data,Nom=Nom,page=page,pageS=pageS,Lpage=Lpage,liste=liste,pageP=pageP,nombre_articles=nombre_articles)
            except:
                return "une Erreur s'est produite. "
        elif request.method=='POST':
            if request.form.get('search'):
                try: 
                    word_to_search = request.form['search']
                    mycursor.execute("SELECT * FROM ((SELECT * FROM `tous_articles` WHERE Nom_table='"+Nom+"') AS "+Nom+") WHERE (`Client` LIKE '%"+word_to_search+"%') OR (`Désignation` LIKE '%"+word_to_search+"%') OR (`PrixUnitaire` LIKE '%"+word_to_search+"%') ORDER BY id DESC")
                    data1 = mycursor.fetchall()
                    connection.commit()
                    return render_template('results.html',id=id,name=name,data1=data1,page=page,Nom=Nom)
                except:
                    return "une Erreur s'est produite. "
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_DB/<string:Nom>/vider',methods=['GET','POST'])
@login_required
def empty(id,name,Nom):
    try:
        mycursor.execute("DELETE FROM `tous_articles` WHERE Nom_table=%s",(Nom,))
        connection.commit()
        return redirect(url_for("artcldb",id=id,name=name))
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_Ajout', methods=['POST', 'GET'])
@login_required
def ajoutartcl(id,name):
    try:
        return render_template('Achat_PROMETI_Articles_Ajout.html',id=id,name=name, data2=data2)
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_Ajout',methods=['POST','GET'])
@login_required
def addall(id,name):
    try:
        if request.method == 'POST':
            try:
                selected = request.form.get('selected')
                client = request.form['client']
                designation = request.form['designation']
                prixunitaire = request.form['prixunitaire']
                mycursor.execute("INSERT INTO `tous_articles` (Nom_table , Client , Désignation , PrixUnitaire) VALUES(%s,%s,%s,%s)",(selected,client,designation,prixunitaire))
                connection.commit()
            except:
                return ("une erreur s'est prduite lors de l'insertion des données, essayez de nouveau.")
            finally:
                return redirect(url_for("artcldb",id=id,name=name))
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route('/9182<int:id>7456/<string:name>/Ajout_specifique_table/<string:Nom_table>',methods=['GET','POST'])
@login_required
def specifictable(id,name,Nom_table):
    try:
        return render_template('Ajout_specifique_table.html',id=id,name=name,Nom_table=Nom_table)
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route('/9182<int:id>7456/<string:name>/Ajout_specifique_table/<string:Nom_table>/ajout',methods=['POST', 'GET'])
@login_required
def ajoutart(id,name,Nom_table):
    try:
        if request.method == 'POST':
            try:
                client = request.form['client']
                designation = request.form['designation']
                prixunitaire = request.form['prixunitaire']
                mycursor.execute("INSERT INTO `tous_articles` (Nom_table , Client , Désignation , PrixUnitaire) VALUES(%s,%s,%s,%s)",(Nom_table,client,designation,prixunitaire))
                connection.commit()
            except:
                return ("une erreur s'est prduite lors de l'insertion des données, essayez de nouveau.")
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"
    finally:
        return redirect(url_for('data',id=id,name=name,Nom=Nom_table,page=1))


@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_DB/<string:Nom_table>/update/<int:id_article>/<int:page>', methods=['POST','GET'])
@login_required
def update(id,name,id_article,Nom_table,page):
    try:
        if request.method == 'POST':
            client = request.form['client']
            designation = request.form['designation']
            prixunitaire = request.form['prixunitaire']
            mycursor.execute("UPDATE `tous_articles` SET Client=%s, Désignation=%s, PrixUnitaire=%s WHERE id=%s AND Nom_table=%s", (client, designation, prixunitaire,id_article,Nom_table))
            connection.commit()
            return redirect(url_for('artcldb',id=id,name=name,page=page))
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"


@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_Articles_DB/<string:Nom_table>/delete/<int:id_article>/<string:Client>/<int:page>', methods=['POST','GET'])
@login_required
def delete(id,name,id_article,Nom_table,Client,page):
    try:
        mycursor.execute("DELETE FROM `tous_articles` WHERE ID=%s AND Nom_table= %s AND Client=%s",(id_article,Nom_table,Client))
        connection.commit()
        return redirect(url_for('artcldb',id=id,name=name,page=page))
    except:
        return "Une erreur s'est produite lors de la suppression de l'article, veillez réessayer ultérieurement"







@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_fournisseurs_DB/Page = <int:page>',methods=['GET','POST'])
@login_required
def data1(id,name,page):
    try:
        mycursor2 = connection.cursor()
        mycursor2.execute("SELECT COUNT(*) FROM `achat_fournisseur`")
        tuple_nombre_fournisseurs = mycursor2.fetchone()
        nombre_fournisseurs = tuple_nombre_fournisseurs[0]
        nombre_pages = math.ceil(nombre_fournisseurs/500)
        liste = list(range(1,nombre_pages+1))
        pageP = page - 1
        if request.method == 'POST':
            try:
                if request.form.get('search'):
                    word_to_search = request.form['search']
                    mycursor.execute("SELECT * FROM `achat_fournisseur` WHERE (`CT_Num` LIKE '%"+word_to_search+"%') OR (`DL_Design` LIKE '%"+word_to_search+"%') OR (`PrixUnitaire` LIKE '%"+word_to_search+"%') OR (`Commerciale` LIKE '%"+word_to_search+"%') OR (`Num_Telephone` LIKE '%"+word_to_search+"%') OR (`Email` LIKE '%"+word_to_search+"%') ORDER BY id DESC")
                    data1 = mycursor.fetchall()
                    connection.commit()
                    return render_template('results1.html',id=id,name=name,data1=data1,page=page)
            except:
                return "Une erreur s'est produite lors du chargement des informations, veillez réessayer ultérieurement"
        elif request.method == 'GET':
            try:
                if page <= 0 :
                    return "<h1 style='text-align:center;'>page not found.</h1>"
                elif page > nombre_pages + 1:
                    return"<h1 style='text-align:center;'>page not found.</h1>"
                else :
                    page2 = 500*pageP
                    mycursor.execute("SELECT * FROM ((SELECT * FROM `achat_fournisseur`) AS achat_fournisseur_REV) ORDER BY id DESC LIMIT 500 OFFSET "+str(page2)+";")
    #                mycursor.execute("(SELECT * FROM `achat_fournisseur` LIMIT 3 OFFSET "+str(page2)+") ORDER BY id DESC")
                    data = mycursor.fetchall()
                    pageS = page + 1
                    Lpage = nombre_pages
                    return render_template('Achat_PROMETI_fournisseurs_DB.html',id=id,name=name,data=data,liste=liste,page=page,pageP=pageP,pageS=pageS,Lpage=Lpage,nombre_fournisseurs=nombre_fournisseurs)
            except:
                return "Une erreur s'est produite lors du chargement des informations, veillez réessayer ultérieurement"
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"

@app.route('/9182<int:id>7456/<string:name>/Achat_PROMETI_fournisseurs_Ajout', methods=['POST', 'GET'])
@login_required
def suppliersadd(id,name):
    try:
        if request.method == 'POST':
            try:
                CT_Num = request.form['ctnum']
                DL_Design = request.form['dldesign']
                PrixUnitaire = request.form['prixunitaire']
                commerciale = request.form['commerciale']
                numtel = request.form['numtel']
                email = request.form['email']
                mycursor.execute("INSERT INTO `achat_fournisseur`" 
                """ ( CT_Num,  DL_Design,  PrixUnitaire, Commerciale,Num_Telephone, Email ) 
                    VALUES(%s,%s,%s,%s,%s,%s)""",(CT_Num,DL_Design,PrixUnitaire,commerciale,numtel,email))
                connection.commit()
                return redirect(url_for("data1",id=id,name=name,page=1))
            except:
                return ("une errue s'est prduite lors de l'insertion des données, essayez de nouveau.")
        return render_template('Achat_PROMETI_fournisseurs_Ajout.html',id=id,name=name,page=1)
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"

@app.route('/9182<int:id>7456/<string:name>/update1/<int:id_suppliers>/<int:page>', methods=['POST','GET'])
@login_required
def update1(id,name,id_suppliers,page):
    try:
        if request.method == 'POST':
            try:
                CT_Num = request.form['ctnum']
                DL_Design = request.form['dldesign']
                PrixUnitaire = request.form['prixunitaire']
                commerciale = request.form['commerciale']
                numtel = request.form['numtel']
                email = request.form['email']
                mycursor.execute("""UPDATE `achat_fournisseur`
                    SET CT_Num=%s, DL_Design=%s, PrixUnitaire=%s,Commerciale=%s,Num_Telephone=%s,Email=%s
                    WHERE id=%s""", (CT_Num,DL_Design,PrixUnitaire,commerciale,numtel,email,id_suppliers))
                connection.commit()
                return redirect(url_for('data1',id=id,name=name,page=page))
            except:
                return "Une erreur s'est produite lors de la modification du fournisseur, veillez réessayer ultérieurement"
        return redirect(url_for('data1',id=id,name=name,page=page))
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"

@app.route('/9182<int:id>7456/<string:name>/delete1/<int:id_suppliers>/<int:page>', methods=['GET'])
@login_required
def delete1(id,name,id_suppliers,page):
    try:
        mycursor.execute("DELETE FROM `achat_fournisseur` WHERE id=%s",(id_suppliers,))
        connection.commit()
        return redirect(url_for('data1',id=id,name=name,page=page))
    except:
       return "Une erreur s'est produite lors de la suppression du fournisseur, veillez réessayer ultérieurement"




@app.route('/Achat PROMETI_Login' ,methods=['GET','POST']) 
def logged_in():
    error= None
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
            username = request.form['username'] 
            password = request.form['password'] 
            nb = list(password)
            cnt = len(nb)
            mycursor.execute("SELECT * FROM `login` WHERE `Email` = %s", (username,)) 
            account = mycursor.fetchall()
            if not username:
                error = 'Email manquant !!'
            elif not password:
                error = 'Mot de Passe manquant !!' 
            elif cnt < 8 :
                error = 'Le Mot de passe est très court (<8)!'
            elif len(account) ==1:
                try:
                    tpl = account[0] 
                    if username != tpl[3]:
                        error = 'Email Incorrect !!'
                    elif not check_password_hash(tpl[4] , password):
                        error = 'Mot de passe Incorrect !!'
                    elif tpl[3] == username and check_password_hash(tpl[4] , password) and cnt > 8: 
                        session['logged_in'] = True
                        session['username'] = username
                        id = tpl[0]
                        name = tpl[2]
                        flash('You were successfully logged in :)')
                        return redirect(url_for('profile',id=id,name=name)) 
                except:
                    error = "Mot de passe incorrect !!"
            else:   
                error = 'On ne dispose pas de cette Adresse Email'
        return render_template('Achat PROMETI_Login.html', error = error) 
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"

@app.route('/logout')
@login_required
def logged_out():
    try:
        session.clear()
        session.pop('logged_in', None)
        return render_template("logout.html")
    except:
        return "<h1 style='text-align:center;'>page not found.</h1>"

    


if __name__ == '__main__' :
    app.run (debug=True)