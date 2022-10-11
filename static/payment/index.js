let public_key = document.getElementById('id_stripe_public_key').value;
let stripe = Stripe(public_key); 
// let stripe = Stripe('pk_test_51LVDiHFR4QsZUb5pbOrLsqC1EyFjDyKyjdWCioeB9yu5uD862wCWUwdClDTx2gsH4ReQIZvh6XJniz3O11KXqybW00unW5awdd'); 
// need publish key 

let form = document.getElementById('payment-form');
console.log(form)

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
      console.log('here')
    ev.preventDefault();

    let full_name = document.getElementById("full_name").value;
    let address1 = document.getElementById("address1").value;
    let post_code = document.getElementById("post_code").value;
    let country = document.getElementById("country").value;
    let city = document.getElementById("city").value;

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
                post_code: post_code
        },
        success: function (json) {
          console.log(json.success)

          stripe.confirmCardPayment(clientsecret, {
              payment_method: {
              card: card,
              billing_details: {
                name: full_name,
                // email: email,
                address: {
                    line1: address1,
                    // state:state,
                    line2: country,
                    line2: post_code,
                    // line2:city,
                },
              },
            }
          }).then(function (result) {
            if (result.error) {
              console.log('payment error')
              console.log(result.error.message);
            } else {
              if (result.paymentIntent.status === 'succeeded'){
                console.log('payment processed')
                window.location.replace("/orders/thank-you/");
              }
            }
          });

        },
      error: function (xhr, errmsg, err) {console.log(errmsg), console.log(err)},
    });

});



