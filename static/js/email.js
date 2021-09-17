if(window.location.pathname == '/contact') {
    document.getElementById('contact-us').addEventListener('submit', function(event) {
        event.preventDefault();
    
        const serviceID = 'service_f9rpwds';
        const templateID = 'template_i5soxme';
    
        emailjs.sendForm(serviceID, templateID, this)
            .then(function() {
                console.log('SUCCESS!');
                document.getElementById("contact-us").reset();
            }, function(error) {
                console.log('FAILED...', error);
                document.getElementById("contact-us").reset();
            });
    });
}
