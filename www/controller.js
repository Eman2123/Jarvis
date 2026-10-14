 eel.init();
 $(document).ready(function () {
    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        // replace the hidden textillate <li>
        
        $(".siri-message .texts li").text(message);
        // re-initialize textillate so it splits into 
        $('.siri-message').textillate('start');
    }
     // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }
 eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }
       
eel.expose(hideLoader);

function hideLoader() {
    $("#Loader").attr("hidden", true);
}



    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {

        $("#Start").attr("hidden", true);

        setTimeout(function () {
            $("#oval").addClass("animate__animated animate__zoomIn");

        }, 1000)
        setTimeout(function () {
            $("#oval").attr("hidden", false);
        }, 1000)
    }


});



