document.getElementById("resetBtn").addEventListener("click", async () => {

    let email = document.getElementById("email").value.trim();
    let newPassword = document.getElementById("newPassword").value.trim();
    let confirmPassword = document.getElementById("confirmPassword").value.trim();

    if(email=="" || newPassword=="" || confirmPassword==""){

        Swal.fire({
            icon:"warning",
            title:"Missing Information",
            text:"Please fill all fields.",
            background:"#101827",
            color:"#fff"
        });

        return;
    }

    let exists = await eel.checkEmail(email)();

    if(!exists){

        Swal.fire({
            icon:"error",
            title:"Email Not Found",
            text:"This email is not registered.",
            background:"#101827",
            color:"#fff"
        });

        return;
    }

    if(newPassword !== confirmPassword){

        Swal.fire({
            icon:"error",
            title:"Password Mismatch",
            text:"Both passwords must be the same.",
            background:"#101827",
            color:"#fff"
        });

        return;
    }

    await eel.updatePassword(email,newPassword)();

    Swal.fire({
        icon:"success",
        title:"Password Updated",
        text:"Your password has been changed successfully.",
        showConfirmButton:false,
        timer:1800,
        background:"#101827",
        color:"#fff"
    });

    setTimeout(()=>{

        window.location.href="login.html";

    },1800);

});