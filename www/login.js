window.onload=function(){

let savedEmail=localStorage.getItem("remember_email");

let savedPassword=localStorage.getItem("remember_password");

if(savedEmail){

document.getElementById("email").value=savedEmail;

document.getElementById("password").value=savedPassword;

document.getElementById("rememberMe").checked=true;

}

}



document.getElementById("loginBtn").addEventListener("click", async () => {

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if(email==="" || password===""){
        alert("Please enter Email and Password");
        return;
    }

    let result = await eel.userLogin(email,password)();

if(result){

    // Remember Me
    const remember = document.getElementById("rememberMe").checked;

    if(remember){

        localStorage.setItem("remember_email", email);

        localStorage.setItem("remember_password", password);

    }
    else{

        localStorage.removeItem("remember_email");

        localStorage.removeItem("remember_password");

    }

    Swal.fire({

        icon:"success",

        title:"Welcome Back!",

        text:"Login Successful",

        showConfirmButton:false,

        timer:1500,

        background:"#101827",

        color:"#fff"

    });

    setTimeout(()=>{

        window.location.href="index.html";

    },1500);

}
else{

    Swal.fire({

        icon:"error",

        title:"Login Failed",

        text:"Invalid Email or Password",

        confirmButtonColor:"#0ea5e9",

        background:"#101827",

        color:"#fff"

    });

}
       
  


}); 




const eye = document.querySelector(".eye");
const password = document.getElementById("password");

eye.addEventListener("click",()=>{

    if(password.type==="password"){

        password.type="text";
        eye.classList.remove("fa-eye");
        eye.classList.add("fa-eye-slash");

    }else{

        password.type="password";
        eye.classList.remove("fa-eye-slash");
        eye.classList.add("fa-eye");

    }

});
