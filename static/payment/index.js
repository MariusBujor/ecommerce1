let public_key = document.getElementById('id_stripe_public_key').value;
let stripe = Stripe(public_key); 

let form = document.getElementById('payment-form');

let elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
let elements = stripe.elements();
let style = {
    base: {
        color: "#000",
        lineHeight: '2.4',
        fontSize: '16px'
    }
};

    let card = elements.create("card", {
      hidePostalCode: true,
      style: style
    });
    card.mount("#card-element");

    card.on('change', function(event) {
    let displayError = document.getElementById('card-errors')
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
    });

    form.addEventListener('submit', function(ev) 
    {
    ev.preventDefault();

    let full_name = document.getElementById("full_name").value;
    let address1 = document.getElementById("address1").value;
    let billing_post_code = document.getElementById("post_code").value;
    let country = document.getElementById("country").value;
    let city = document.getElementById("city").value;
    let email = document.getElementById("user_email").value;

    $.ajax({
            type: "POST",
            url: '/orders/add/',
            data: {
                order_key: clientsecret,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: "post",
                full_name: full_name,
                address1: address1,
                city: city,
                country: country,
                post_code: billing_post_code
        },
        success: function (json) {

          stripe.confirmCardPayment(clientsecret, {
              payment_method: {
              card: card,
              billing_details: {
                name: full_name,
                email: email,
                address: {
                    line1: address1,
                    city: city,
                    country: country,
                    postal_code: billing_post_code,
                },
              },
            }
          }).then(function (result) {
            if (result.error) {
              console.log(result.error.message);
            } else {
              if (result.paymentIntent.status === 'succeeded'){
                window.location.replace("/orders/thank-you/");
              }
            }
          });

        },
      error: function (xhr, errmsg, err) {console.log(errmsg), console.log(err)},
    });

});



