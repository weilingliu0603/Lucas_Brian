from flask import *
import sqlite3

app=Flask(__name__)


def get_db():
    db = sqlite3.connect('Salondatabase.db')
    db.row_factory = sqlite3.Row
    return db
       

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/AddMember')
def AddMem():
    return render_template('AddMem.html')
@app.route('/Memberadded', methods=['POST']) ##new entry
def Memadded(): 
    M = request.form['MemberID']
    F = request.form['Fullname']
    G = request.form['Gender']
    E = request.form['Email']
    C = request.form['ContactNo']
    A = request.form['Address']
    db = get_db()
    db.execute('INSERT into MEMBER (MemberID, MemberName, Gender, Email, Contact, Address) VALUES (?,?,?,?,?,?)',(M,F,G,E,C,A))
    db.commit()
    db.close()
    return render_template('Memberadded.html',F=F)

       
@app.route('/AddTrans')
def AddTrans():
    return render_template('AddTrans.html')
@app.route('/Transadded',methods=['POST'])
def Transadded():
    A = request.form['MemberID']
    N = request.form['Name']
    D = request.form['Date']
    S = request.form['Short']
    M = request.form['Medium']
    L = request.form['Long']
    C = request.form['Colour']
    H = request.form['Half']
    F = request.form['Full']
    P = request.form['Perm']
    R = request.form['Rebounding']
    T = request.form['Treatment']
    lst=[S,M,L,C,H,F,P,R,T]
    db = get_db()
    Service = db.execute("SELECT * FROM SERVICE").fetchall()
    total=0
    InvoiceID=len(db.execute("SELECT InvoiceID FROM TRANSACT").fetchall())+1
    for i in range(len(lst)):
        if lst[i]=='1':
            total+=Service[i][1]
            db.execute('INSERT into TRANSACTIONDETAILS(Type,InvoiceID) VALUES(?,?)',(Service[i][0],InvoiceID))
            db.commit()
    if A!='00':
        total='{:0,.2f}'.format(total*0.9)
        db.execute('INSERT into TRANSACT (InvoiceID, Date, Name, MemberID, Total_amount) VALUES (?,?,?,?,?)',(str(InvoiceID),D,N,A,total))
        db.commit()
    else:
        total='{:0,.2f}'.format(total)
        db.execute('INSERT into TRANSACT (InvoiceID, Date, Name, MemberID, Total_amount) VALUES (?,?,?,?,?)',(str(InvoiceID),D,N,'0',total))
        db.commit()
    db.close()
    return render_template('Transadded.html')



@app.route('/Trans')
def Trans(): 
    return render_template('Trans.html')
       
@app.route('/Trans/Monthly')
def Monthly():
    return render_template("Monthly.html")

@app.route('/Trans/Daily/MonthlyTrans',methods=["POST"])
def MonthlyTrans():
    Month=request.form["Month"]
    Year=request.form["Year"]
    endmonth=str(int(Month)+1).zfill(2)+'/01/'+Year
    db = get_db()
    rows = db.execute('SELECT * FROM TRANSACT WHERE Date>=(?) AND Date<(?)',(Month,endmonth)).fetchall()
    db.close()
    return render_template('MonthlyTrans.html', rows=rows)

@app.route('/Trans/Daily')
def Daily():
    return render_template("Daily.html")

@app.route('/Trans/Daily/DailyTrans',methods=["POST"])
def DailyTrans():
    Day=request.form["Day"]
    Month=request.form["Month"]
    Year=request.form["Year"]
    Date=Month+'/'+Day+'/'+Year
    db = get_db()
    rows = db.execute('SELECT * FROM TRANSACT WHERE Date=(?)',(Date,)).fetchall()
    db.close()
    return render_template('DailyTrans.html', rows=rows)

@app.route('/Trans/Member')
def Member():
    return render_template("Member.html")
@app.route('/Trans/Member/MemberHist',methods=['POST'])
def MemberHist():
    MemberID=request.form["MemberID"]
    db=get_db() 
    rows = db.execute('SELECT * FROM TRANSACT WHERE MemberID=(?)',(MemberID)).fetchall()
    db.close()
    return render_template("MemberHist.html",rows=rows)

@app.route('/Update')
def Update():
    return render_template('Update.html')
@app.route('/Memberupdate', methods=['POST']) ##new entry
def Memupdate(): 
    M = request.form['MemberID']
    E = request.form['Updated Email']
    C = request.form['Updated ContactNo']
    db = get_db()
    check=db.execute("SELECT MemberID FROM MEMBER WHERE MEMBERID=(?)",(M,)).fetchall()
    
    if len(check)==1:
        if E=='Enter Email' and C=='Enter ContactNo':
            return render_template("/Update.html")
        else:
            if E!='Enter Email':
                db.execute("UPDATE MEMBER SET Email=(?) WHERE MEMBERID=(?)",(E,M))
                db.commit()
            if C!='Enter ContactNo':
                db.execute("UPDATE MEMBER SET Contact=(?) WHERE MEMBERID=(?)",(C,M))
                db.commit()
        return render_template("Updatesuccess.html",M=M)
    else:
        return render_template("Updateunsuccess.html",M=M)
    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)



