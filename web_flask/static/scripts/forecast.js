$(document).ready(function () {
    const forecastURL = 'https://api.openweathermap.org/data/2.5/forecast?';
    const units = 'imperial'; // can be imperial or metric
    let temperatureSymbol = units === 'imperial' ? "°F" : "°C";

    const apiKey = '7643c850c0f525a188fcc34a148f0f98'; // Make sure to replace this with your actual API key
    const weatherContainer = document.getElementById('weatherF');
    const city = document.getElementById('cityF');

    $('#forecast').click(function () {
        const customerInputCity = $('#cityInputF').val();
        const cnt = 10;
        const url = `${forecastURL}appid=${apiKey}&q=${customerInputCity}&units=${units}&cnt=${cnt}`;

        weatherContainer.innerHTML = '';

        $.get(url, function (data) {
            if (data.cod === '400' || data.cod === '404') {
                $('#errorF').html("<p>Not a valid city. Please input another city</p>");
                return;
            }

            data.list.forEach(hourlyWeatherData => {
                const hourlyWeatherDataDiv = createWeatherDescription(hourlyWeatherData);
                weatherContainer.appendChild(hourlyWeatherDataDiv);
            });
    
            // Display city name based on latitude and longitude
            city.innerHTML = `Hourly Weather for ${data.city.name}`;
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

    function createWeatherDescription(weatherData) {
        const { main, weather, dt } = weatherData;
    
        const description = document.createElement("div");
        const convertedDateAndTime = convertToLocalTime(dt);
    
        description.innerHTML = `
            <div class="weather_description">${main.temp}${temperatureSymbol} - ${weather[0].description} - ${convertedDateAndTime.substring(10)} - ${convertedDateAndTime.substring(5, 10)}</div>
        `;
        return description;
}
});