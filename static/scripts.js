$(document).ready(function() {
    $('#prediction-form').on('submit', function(event) {
        event.preventDefault();
        
        // Show loading state
        $('#result').html('<div class="loading">Making prediction...</div>');
        
        // Get form values
        const weather = $('#weather').val();
        const temperature = $('#temperature').val();
        const humidity = $('#humidity').val();
        
        // Log the values being sent
        console.log('Sending prediction request:', { weather, temperature, humidity });

        $.ajax({
            url: '/predict',
            method: 'POST',
            data: {
                weather: weather,
                temperature: temperature,
                humidity: humidity
            },
            success: function(response) {
                console.log('Received response:', response);
                if (response.success && response.prediction) {
                    const resultClass = response.prediction === 'Yes' ? 'positive' : 'negative';
                    $('#result').html(`
                        <div class="prediction-result ${resultClass}">
                            <h3>Prediction Result:</h3>
                            <p class="prediction">${response.prediction}</p>
                            <p class="explanation">${response.explanation}</p>
                            <div class="conditions">
                                <p><strong>Weather:</strong> ${weather}</p>
                                <p><strong>Temperature:</strong> ${temperature}</p>
                                <p><strong>Humidity:</strong> ${humidity}</p>
                            </div>
                        </div>
                    `);
                } else {
                    $('#result').html(`
                        <div class="error">
                            <p>${response.error || 'Invalid response from server'}</p>
                            ${response.details ? `<p class="error-details">Details: ${response.details}</p>` : ''}
                        </div>
                    `);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                let errorMessage = 'Error making prediction. Please try again.';
                try {
                    const response = JSON.parse(xhr.responseText);
                    if (response.error) {
                        errorMessage = response.error;
                    }
                } catch (e) {
                    console.error('Error parsing response:', e);
                }
                $('#result').html(`
                    <div class="error">
                        <p>${errorMessage}</p>
                        <p class="error-details">Details: ${error}</p>
                    </div>
                `);
            }
        });
    });
});
