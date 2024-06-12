$(document).ready(function () {
    const apiKey = '7643c850c0f525a188fcc34a148f0f98';
    const baseURL = 'https://api.openweathermap.org/data/2.5/weather?';
    
    $('.middle-section .state #realTime').click(function () {
        const customerInputCity = $('#cityInput').val();
        const url = `${baseURL}appid=${apiKey}&q=${customerInputCity}`;

        $.get(url, function (data) {
            if (data.cod === '400' || data.cod === '404') {
                $('#error').html("<p>Not a valid city. Please input another city</p>");
                return;
            }

            function kelvinCelsius(Kelvin) {
                const celsius = Kelvin - 273.15;
                const fahrenheit = celsius * (9 / 5) + 32;
                return [celsius, fahrenheit];
            }

            const kelvin = data['main']['temp'];
            const [celsius_temp, fahrenheit_temp] = kelvinCelsius(kelvin);
            const sunrise = convertToLocalTime(data['sys']['sunrise']);
            const sunset = convertToLocalTime(data['sys']['sunset']);

            const weatherInfo = `
                <p>Temperature: ${celsius_temp.toFixed(2)} C or ${fahrenheit_temp.toFixed(2)} F</p>
                <p>Feels Like: ${data.main.feels_like} K</p>
                <p>Weather Description: ${data.weather[0].description}</p>
                <p>Humidity: ${data.main.humidity} %</p>
                <p>Sun rises in ${customerInputCity}: ${sunrise}</p>
                <p>Sun sets in ${customerInputCity}: ${sunset}</p>
            `;
            $('#weather').html(weatherInfo);
        });
    });

    function convertToLocalTime(dt) {
        const date = new Date(dt * 1000);

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours() % 12 || 12).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        const period = date.getHours() >= 12 ? 'PM' : 'AM';

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds} ${period}`;
    }

});