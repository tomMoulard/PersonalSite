function setup() {
    noCanvas();

    // Wait for RiveScript to be available
    let retryCount = 0;
    const maxRetries = 50; // 5 seconds max

    function initBot() {
        if (typeof RiveScript === 'undefined') {
            retryCount++;
            if (retryCount > maxRetries) {
                return;
            }
            setTimeout(initBot, 100);
            return;
        }

        let bot = new RiveScript();
        let conv = "";
        //bot.loadFile("http://tom.moulard.org/assets/brains/EN-tom.rive", brainReady, brainError);
        bot.loadFile("/assets/brains/EN-tom.rive")
            .then(brainReady)
            .catch(brainError);

        // let button = select("#submit");
        let user_input = select('#user_input');
        let response = select("#dialogue");

        if (user_input && response) {

            user_input.changed(function (e) {
                    ask(user_input.value());
                    user_input.value("");
            });

            // Also add keypress event for Enter key
            user_input.input(function (e) {
                if (e.keyCode === 13) { // Enter key
                    ask(user_input.value());
                    user_input.value("");
                }
            });
        } else {
            console.log("ERROR: Could not find chatbot elements!");
        }
        function brainReady(){
            bot.sortReplies();
        }
        function brainError(error){
            console.log("Chat bot ERROR!", error);
        }
        function ask(things){
            things = betterstr(things);
            conv += "<font color='blue'><p><b>You</b>: " + things + "</p></font>";
            response.html(conv);
            console.log("User asked:", things);
            bot.reply("local-user", things).then(function(reply) {
                console.log("Bot replied:", reply);
                anwser(reply);
            }).catch(function(error) {
                console.log("Bot reply error:", error);
                anwser("Sorry, I had trouble understanding that.");
            });
        }
        function anwser(things){
            conv += "<font color='red'><p><b>Bot</b>: " + things + "</p></font>";
            response.html(conv);
        }
        function betterstr(inpu){
            return inpu.replace(/</g, "&lt;")
                       .replace(/>/g, "&gt;")
                       .replace(/\'/g, "&apos;")
                       .replace(/\"/g, "&apos;&apos;");
        }
    }

    // Start the bot initialization
    initBot();
}
