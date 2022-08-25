let stripe = Stripe('pk_test_51LVDiHFR4QsZUb5pbOrLsqC1EyFjDyKyjdWCioeB9yu5uD862wCWUwdClDTx2gsH4ReQIZvh6XJniz3O11KXqybW00unW5awdd'); 
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

    let custName = document.getElementById("custName").value;
    console.log(custName)
    let custAdd = document.getElementById("custAdd").value;
    let postCode = document.getElementById("postCode").value;

    $.ajax({
            type: "POST",
            url: '/orders/add/',
            data: {
                order_key: clientsecret,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: "post",
                full_name: custName,
                custAdd: custAdd,
        },
        success: function (json) {
          console.log(json.success)

          stripe.confirmCardPayment(clientsecret, {
              payment_method: {
              card: card,
              billing_details: {
                address: {
                    line1: custAdd
                },
                name: custName
              },
            }
          }).then(function (result) {
            if (result.error) {
              console.log('payment error')
              console.log(result.error.message);
            } else {
              if (result.paymentIntent.status === 'succeeded'){
                console.log('payment processed')
                window.location.replace("/payment/orderplaced/");
              }
            }
          });

        },
      error: function (xhr, errmsg, err) {console.log(errmsg), console.log(err)},
    });

});



