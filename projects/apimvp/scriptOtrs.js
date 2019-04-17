var cpf = document.getElementById("DynamicField_CPF");
var firstname = document.getElementById("DynamicField_firstname");
var lastname = document.getElementById("DynamicField_lastname");
var login = document.getElementById("DynamicField_login");
var department = document.getElementById("DynamicField_department");
var rg = document.getElementById("DynamicField_rg");
var room = document.getElementById("DynamicField_room");
var phone = document.getElementById("DynamicField_phone");
var ticketid = document.getElementById("TicketID");
var ticketnumber = document.getElementById("TicketNumber");
var subject = document.getElementById("Subject");
var richtext = document.getElementById("RichText");

function addUser() {
    if (subject.value.length != 0 && RichText.value.length != 0 ){
        $.ajax({
            url: "http://srv095:5002/checkuser",
            type: "POST",
            data: JSON.stringify({
                login_p: login.value
            }),
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                var loginResponse = response.login;
                console.log('Retreived data: ', loginResponse);
                if (loginResponse === undefined) {
                    // alert("Usuário não existe!")
                    $.ajax({
                        url: "http://srv095:5002/adduser",
                        type: "POST",
                        data: JSON.stringify({
                            cpf_p: cpf.value,
                            firstname_p: firstname.value,
                            lastname_p: lastname.value,
                            login_p: login.value,
                            department_p: department.value,
                            rg_p: rg.value,
                            room_p: room.value,
                            phone_p: phone.value
                        }),
                        contentType: "application/json",
                        dataType: "json",
                        success: function () {
                            addUserDB();
                        }
                    });
                } else {
                    alert("Usuário existe ou já foi inserido! Usuário informado: " + login.value + " Usuário econtrado: " + loginResponse);
                }
            }
        });
    } else {
        alert("Campos Obrigatórios, informe-os!");
    }
}

function addUserDB() {
    $.post("http://srv095/appmvp/addUser.php", {
        cpf_p: cpf.value,
        firstname_p: firstname.value,
        lastname_p: lastname.value,
        login_p: login.value,
        department_p: department.value,
        rg_p: rg.value,
        room_p: room.value,
        phone_p: phone.value,
        ticketid_p: ticketid.value,
        ticketnumber_p: ticketnumber.value
    });
}

