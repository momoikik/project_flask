<form method="post" action="{{url_for('Log_in')}}" style="display: flex;">
        <input type="text" autofocus="autofocus" name="Email" >
         <input type="number" autofocus="autofocus" name="password" >
        <input  formaction="/Log_in">
        </form></a>

@app.route('/Log_in', methods=['GET', 'POST'])
def Log():
    if request.method == 'POST':
        form = request.form
        search_password = form['password']
        search_Email = form['Email']
        search_br= "%{0}%".format(search_password,search_Email)
        broser_data = Password.query.filter(Password.password.Name.all())

        return render_template('Log_in.html', broser_data=broser_data, legend="Search Results")
    else:
        return redirect("/Home_page")