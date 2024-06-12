document.addEventListener("DOMContentLoaded", function () {
    function updateDate () {
        const dateContainer = document.getElementById('day');
        const date = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = date.toLocaleDateString(undefined, options);
        dateContainer.innerHTML = `<p>${formattedDate}</p>`
    }

    updateDate();
})

$(document).ready(function () {
    $('.upper-section button').click(function () {
        const weather = `
        <p>Season: Rainy season</p>
        <p>Weather: light season</p>
        <p>Expected highest Temperature: 25 C</p>
        <p>Expected lowest Temperature: 18 C</p>
        <p>Activities: Growing Season</p>
        `;
        $('#season').html(weather);
    });
});