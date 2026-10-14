document.getElementById("registerBtn").addEventListener("click", async () => {

    let firstName = document.getElementById("firstName").value.trim();
    let lastName = document.getElementById("lastName").value.trim();
    let email = document.getElementById("email").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let password = document.getElementById("password").value.trim();
    let confirmPassword = document.getElementById("confirmPassword").value.trim();

    if(firstName=="" || lastName=="" || email=="" || phone=="" || password=="" || confirmPassword==""){

        Swal.fire({
            icon:"warning",
            title:"Missing Information",
            text:"Please fill all fields.",
            background:"#101827",
            color:"#fff"
        });

        return;
    }

    if(password !== confirmPassword){

        Swal.fire({
            icon:"error",
            title:"Password Mismatch",
            text:"Passwords do not match.",
            background:"#101827",
            color:"#fff"
        });

        return;
    }

    let fullName = firstName + " " + lastName;

    let result = await eel.userRegister(
    firstName,
    lastName,
    email,
    phone,
    password
)();



    if(result){

        Swal.fire({
            icon:"success",
            title:"Account Created",
            text:"Registration Successful",
            showConfirmButton:false,
            timer:1500,
            background:"#101827",
            color:"#fff"
        });

        setTimeout(()=>{
            window.location.href="login.html";
        },1500);

    }

    else{

        Swal.fire({
            icon:"warning",
            title:"Email Already Exists",
            text:"Please use another email.",
            background:"#101827",
            color:"#fff"
        });

    }

});

document.querySelectorAll(".eye").forEach((eye)=>{

    eye.onclick=function(){

        const input=this.previousElementSibling;

        if(input.type==="password"){

            input.type="text";
            this.classList.replace("fa-eye","fa-eye-slash");

        }

        else{

            input.type="password";
            this.classList.replace("fa-eye-slash","fa-eye");

        }

    }

});