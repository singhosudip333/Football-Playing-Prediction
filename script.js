$(document).ready(function() {
    $('#prediction-form').on('submit', function(event) {
        event.preventDefault();

        $.ajax({
            url: '/predict',
            method: 'POST',
            data: {
                weather: $('#weather').val(),
                temperature: $('#temperature').val(),
                humidity: $('#humidity').val()
            },
            success: function(response) {
                $('#result').text('Prediction: ' + response.prediction);
            }
        });
    });
});
