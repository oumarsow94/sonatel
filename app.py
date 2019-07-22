import psycopg2 as psy
import psycopg2.extras

from flask import Flask, render_template,url_for,request,flash, redirect, jsonify,session
from functools import wraps
import json
import datetime


app = Flask(__name__)
app.secret_key = "flash message"

#----------------------Partie connexion à la base de données--------------------
def connectToDB():
    try:
        #  connectionString = 'dbname=music user=postgres password=kirbyk9 host=localhost'
        connection = psy.connect(user='postgres',
                                host='localhost',
                                port='5432',
                                password='Fatimata94&',
                                database = 'sa'
                                )
        return connection
    except(Exception) as error:

        print("Probleme de connexion au serveur PostgreSQL", error)
connection = connectToDB()
curseur = connection.cursor()


#----------------------Partie Accueil pagination--------------------


# create the appliction object
app = Flask(__name__)

app.secret_key = "my precious"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#use decorate to link the function to a url


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['user'] != 'oumar' or request.form['password'] != 'fa':
            error = 'Invalid credentals. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!') 
            return redirect(url_for('test'))
    return render_template('login.html', error=error)
''' 
@app.route('/home')
def home():
    return render_template('index.html') # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html') '''


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!') 
    return redirect(url_for('login'))

''' @app.route("/home")
def home():
	return render_template("test.html") '''



@app.route('/test')
def test():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_apprenant, matricule, prenom,nom,date_naissance,telephone,mail,statut,nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo AND apprenant.statut='Inscrit'")
        d = curseur.fetchall()
        curseur.close()
        connection.close()
    
        #return render_template('dt.html', students=d)
        return render_template('dt.html', students=d)

#----------------------Partie Inscription pagination--------------------
@app.route('/inscription')
def inscription():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_apprenant, matricule, prenom,nom,telephone,mail,statut,nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo AND apprenant.statut='Inscrit'")
        data = curseur.fetchall()
        curseur.close()
        connection.close()

        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT * FROM promo where date_debut>DATE( NOW() )")
        data3 = curseur.fetchall()
        curseur.close()
        connection.close()

        return render_template('inscription.html', students = data, apprenant = data3)


@app.route('/modification')
def modifier():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_apprenant, matricule, prenom,nom,date_naissance,telephone,mail,statut,nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo AND apprenant.statut='Inscrit'")
        data = curseur.fetchall()
        curseur.close()
        connection.close()

        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT * FROM promo where date_debut>DATE( NOW() )")
        data1 = curseur.fetchall()
        curseur.close()
        connection.close()
        return render_template('mod.html', students = data , student = data1)


#----------------------------Update----------------------------------------------------------------
@app.route('/update',methods=['POST','GET'])
def update():

        if request.method == 'POST':
                id_data = request.form['id_a'] 
                mat = request.form['mat'] 
                name = request.form['Fname']
                
                lname = request.form['lname']
                nais = request.form['naissance']
                phone = request.form['MNum']
                email = request.form['email']
                promo = request.form['promo']
                connection = connectToDB()
                curseur = connection.cursor()
                curseur.execute("""
                UPDATE apprenant
                SET matricule=%s, prenom=%s,nom=%s,date_naissance=%s, telephone=%s, mail=%s,id_promo=%s
                WHERE id_apprenant=%s
                """, (mat, name, lname, nais, phone, email, promo,id_data))
                
                flash("Data Updated Successfully")
                connection.commit()
                return redirect(url_for('modifier'))

@app.route('/suspendre')
def suspendre():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_apprenant, matricule, prenom,nom,date_naissance,telephone,mail,statut,nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo AND apprenant.statut='Inscrit'")
        data7 = curseur.fetchall()
        curseur.close()
        connection.close()

       
        return render_template('suspendre.html', students = data7 )

@app.route('/suspendu')
def suspendu():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_apprenant, matricule, prenom,nom,date_naissance,telephone,mail,statut,nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo AND apprenant.statut='Suspendu'")
        datas = curseur.fetchall()
        curseur.close()
        connection.close()

       
        return render_template('app_sus.html', students = datas )

@app.route('/update_sr/<string:id_data>', methods = ['GET'])
def update_sr(id_data):
        flash("Record Has Been canceled Successfully")
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("UPDATE apprenant SET statut ='Inscrit' WHERE id_apprenant=%s", (id_data,))
    
                
        
        connection.commit()
        return redirect(url_for('suspendu'))
#----------------------------Update----------------------------------------------------------------

@app.route('/update_s/<string:id_data>', methods = ['GET'])
def update_s(id_data):
        flash("Record Has Been canceled Successfully")
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("UPDATE apprenant SET statut ='Suspendu' WHERE id_apprenant=%s", (id_data,))
    
                
        
        connection.commit()
        return redirect(url_for('suspendre'))
#------------------------------------------------------------------------------------------------------------
@app.route('/annuler')
def annuler():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_apprenant, matricule, prenom,nom,date_naissance,telephone,mail,statut,nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo AND apprenant.statut='Inscrit'")
        data7 = curseur.fetchall()
        curseur.close()
        connection.close()

       
        return render_template('annuler.html', students = data7 )


@app.route('/update_a/<string:id_data>', methods = ['GET'])
def update_a(id_data):
        flash("Record Has Been canceled Successfully")
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("UPDATE apprenant SET statut ='Annule' WHERE id_apprenant=%s", (id_data,))
    
                
        
        connection.commit()
        return redirect(url_for('annuler'))
#----------------------Partie Promotion pagination--------------------
@app.route('/promo')
def promo():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_promo,nom_promo,date_debut,date_fin,nom_ref FROM promo,referentiel WHERE promo.id_ref=referentiel.id_ref;")
        data = curseur.fetchall()
        curseur.close()
        connection.close()

        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT * FROM referentiel")
        data2 = curseur.fetchall()
        curseur.close()
        connection.close()
        return render_template('promo.html', students = data, ref=data2)
    


#----------------------Partie Referentiel pagination--------------------
@app.route('/ref')
def ref():

        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT * FROM referentiel")
        data = curseur.fetchall()
        curseur.close()
        connection.close()
        return render_template('referent.html', students = data)
        #return render_template('nou_ref.html')





#inserer ref 
@app.route('/ref', methods = ['POST'])
def insert_ref():
        
        if request.method == "POST":
                
                name = request.form['ref']
                connection = connectToDB()
                curseur = connection.cursor()
                curseur.execute("SELECT nom_ref FROM referentiel")
                data = curseur.fetchall()
        
                connection.commit()
                

                ctr=False
                for i in data:
                        if i[0] == name:
                                ctr=True
                                break
                if ctr== True:
                        flash('nom existe deja')
                        return redirect(url_for('ref'))
                else:

                        flash("Referentiel Inserted Successfully") 
                        curseur.execute("INSERT INTO referentiel (nom_ref) VALUES (%s)", (name,))
                        #curseur.execute("INSERT INTO data (firstname) VALUES (%s, )", name)
                        connection.commit()
                        return redirect(url_for('ref'))
        return redirect(url_for('ref'))

@app.route('/referentiel')
def referentiel():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT * FROM referentiel")
        data = curseur.fetchall()
        curseur.close()
        connection.close()
        return render_template('modif_ref.html', students = data)

@app.route('/modif_ref',methods=['POST','GET'])
def modif_ref():

        if request.method == 'POST':
                id_data = request.form['id'] 
                nom = request.form['ref'] 
                connection = connectToDB()
                curseur = connection.cursor()
                curseur.execute("""
                UPDATE referentiel
                SET nom_ref=%s
                WHERE id_ref=%s
                """, (nom,id_data))
                
                flash("Referentiel Updated Successfully")
                connection.commit()
                return redirect(url_for('referentiel'))
        

#inserer promo
@app.route('/promo', methods = ['POST'])
def insert_promo():
    if request.method == "POST":
        
        promo = request.form['promo']
        debut = request.form['db']
        fin = request.form['df']
        ref = request.form['ref']
        
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT nom_promo FROM promo")
        dp = curseur.fetchall()

        connection.commit()
        

        ctr=False
        for i in dp:
                if i[0] == promo:
                        ctr=True
                        break
        if ctr== True:
                flash('cette promo existe deja')
                return redirect(url_for('promo'))
        else:
                flash("Promo Inserted Successfully")
                curseur.execute("INSERT INTO promo (nom_promo, date_debut, date_fin, id_ref) VALUES (%s, %s, %s, %s)", (promo, debut,fin, ref))
                #curseur.execute("INSERT INTO data (firstname) VALUES (%s, )", name)
                connection.commit()
                return redirect(url_for('promo'))
        return redirect(url_for('promo'))

@app.route('/promotion')
def promotion():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_promo,nom_promo,date_debut,date_fin,nom_ref FROM promo,referentiel WHERE promo.id_ref=referentiel.id_ref;")
        data = curseur.fetchall()
        curseur.close()
        connection.close()

        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT * FROM referentiel")
        data5 = curseur.fetchall()
        curseur.close()
        connection.close()
        return render_template('modif_promo.html', students = data , promo = data5)

@app.route('/modif_promo',methods=['POST','GET'])
def modif_promo():

        if request.method == 'POST':
                id_data = request.form['id'] 
                pro = request.form['pro'] 
                debut = request.form['debut']
                
                fin = request.form['fin']
                
                promo = request.form['promo']
                connection = connectToDB()
                curseur = connection.cursor()
                curseur.execute("""
                UPDATE promo
                SET nom_promo=%s, date_debut=%s,date_fin=%s,id_ref=%s
                WHERE id_promo=%s
                """, (pro, debut, fin, promo,id_data))
                
                flash("Promo Updated Successfully")
                connection.commit()
                return redirect(url_for('promotion'))

@app.route('/listpromotion')
def listpromotion():
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT id_promo,nom_promo,date_debut,date_fin,nom_ref FROM promo,referentiel WHERE promo.id_ref=referentiel.id_ref;")
        datp = curseur.fetchall()
        curseur.close()
        connection.close()

        # connection = connectToDB()
        # curseur = connection.cursor()
        # curseur.execute("SELECT matricule, prenom,nom,date_naissance,telephone,mail,statut,nom_promo,nom_ref FROM apprenant, promo,referentiel WHERE apprenant.id_promo=promo.id_promo AND promo.id_ref=referentiel.id_ref AND apprenant.statut='Inscrit'")
        # datl = curseur.fetchall()
        # curseur.close()
        # connection.close()
        return render_template('list.html', students=datp)

@app.route('/listepromo/<string:id_data>', methods= ['GET'])
def listepromo(id_data):

                
        connection = connectToDB()
        curseur = connection.cursor()
        
        curseur.execute("SELECT matricule, prenom,nom,date_naissance,telephone,mail,statut FROM apprenant WHERE apprenant.id_promo=%s AND apprenant.statut='Inscrit'",(id_data,))
        datl = curseur.fetchall()
        curseur.close()
        connection.close()
        return render_template('lister.html', students = datl)
        #return redirect(url_for('listpromotion'))

#inserer apprenant
@app.route('/inscription', methods = ['POST'])
def insert():

    if request.method == "POST":

        #mat = request.form['mat']
        name = request.form['Fname']
        
        lname = request.form['lname']
        nais = request.form['naissance']
        phone = request.form['MNum']
        email = request.form['email']
        #sta = request.form['statut']
        promo = request.form['promo']

        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute('SELECT MAX(id_apprenant) FROM apprenant')
        x=curseur.fetchone()
        curseur.close()
       
        m = x[0]+1
        mat = "SA-"+str(m)

        #------date_naissance-----
        connection = connectToDB()
        curseur = connection.cursor()
        curseur.execute("SELECT mail,telephone FROM apprenant")
        naiss = curseur.fetchall()

        connection.commit()
                

        ctr=True
        for i in naiss:
                if i[0] == email or i[0==phone]:
                        ctr=True
                        break
        if ctr == True:
                flash("Tu es deja inscrit")
                return redirect(url_for('inscription'))
        else:
        #-------------fin---------------------
                flash("apprenat Inserted Successfully")
                curseur.execute("INSERT INTO apprenant (matricule, prenom,nom, date_naissance, telephone, mail, id_promo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (mat, name, lname, nais, phone, email, promo))
                #curseur.execute("INSERT INTO data (firstname) VALUES (%s, )", name)
                connection.commit()
                return redirect(url_for('inscription'))
        return redirect(url_for('inscription'))




if __name__ == '__main__':
    app.run(debug=True, port=3000)