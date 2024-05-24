$(document).ready(function() {
    function updateImages(item1, item2) {
        $("#item1-img").attr("src", "{{ url_for('static', filename='') }}" + item1[0]);
        $("#item1-description").text(item1[2]);
        $("#item2-img").attr("src", "{{ url_for('static', filename='') }}" + item2[0]);
        $("#item2-description").text(item2[2]);
    }

    function handleChoice(choice) {
        $.ajax({
            type: "POST",
            url: "/ab_testing_images",
            data: { choice: choice },
            dataType: 'json', // Expect JSON response
            success: function(response) {
                $("#message").html("<p class='text-success'>" + response.message + "</p>");
                updateImages(response.item1, response.item2);
            },
            error: function() {
                $("#message").html("<p class='text-danger'>An error occurred.</p>");
            }
        });
    }

    $("#item1-button").click(function() {
        handleChoice("item1");
    });

    $("#item2-button").click(function() {
        handleChoice("item2");
    });
});