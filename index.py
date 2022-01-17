from flask import Flask,render_template,request,redirect,url_for,flash
from functions import db as db
app = Flask(__name__)


# settings
app.secret_key = 'mysecretkey'

#Main window
@app.route('/')
def invoice():
    data,locationsData,packagesData,paymentMethods = db.getGeneralData()
    return render_template('invoice.html',clients = data,locations = locationsData,packages = packagesData,payments = paymentMethods)

    
@app.route('/invoice/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    data,locationsData,packagesData,paymentMethods = db.getGeneralDataForUpdate(id)
    return render_template('edit-contact.html', client = data[0],locations = locationsData,packages = packagesData,payments = paymentMethods)

@app.route('/invoice/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        re = request.form.to_dict()
        fullname = re['fullname']
        phone = re['phone']
        email = re['email']
        adress = re['adress']
        location = re['location']
        package = re['package']
        payment = re['paymentId']
        if missingMandatoryParameters(re):
                return redirect(url_for('invoice'))
        
        db.updateUserData(fullname,phone,email,adress,location,package,payment,id)
        flash('Contact Updated Successfully')
        return redirect(url_for('invoice'))
    
def missingMandatoryParameters(Parameters):
    error = False
    for name,parameter in Parameters.items():
        if(len(parameter) < 1):
            flash('Error - Mandatory parameter Missing: '+ name.capitalize())
            error = True
    return error

def getClientIdByAdress(adress):
    currentId = db.getClientIdFromAdress(adress)
    return currentId
                       
#Create Contact    
@app.route('/invoice/add', methods = ['POST'])
def invoice_add():
    if request.method == 'POST':
        re = request.form.to_dict()
        fullname = re['fullname']
        phone = re['phone']
        email = re['email']
        adress = re['adress']
        location = re['location']
        package = re['package']
        payment = re['paymentId']
        if missingMandatoryParameters(re):
            return redirect(url_for('invoice'))

        db.addClient(fullname,phone,email,adress,location,package,payment)
        
        flash('Contact added sucessfully')
        return redirect(url_for('invoice'))

#Delete contact        
@app.route('/invoice/delete/<string:id>')
def invoice_delete(id):
    db.deleteClient(id)
    flash('Sucessfully deleted')
    return redirect(url_for('invoice'))


if __name__ == '__main__':
    app.run(port = 3000,debug=True)