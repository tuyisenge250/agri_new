document.addEventListener('DOMContentLoaded', () => {
    const img = document.querySelector('#imageUploadTrigger img');
    const section = document.querySelector('#imageUploadSection');

    img.addEventListener('click', (event) => {
        event.preventDefault();
        section.innerHTML = '<input type="file" name="image">';
    });
});
