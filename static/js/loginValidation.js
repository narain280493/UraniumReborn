/**
 * Created by ranganathan on 11/4/16.
 */
$(document).ready(function() {

    $('#loginform').bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },

            fields: {
                'useremail': {
                    validators: {
                        notEmpty: {
                            message: 'Please supply your email address'
                        },
                        emailAddress: {
                            message: 'Please supply a valid email address'
                        }
                    }
                },


                'password': {
                    validators: {

                        stringLength: {
                            min: 6,
                        },

                        notEmpty: {
                            message: 'The password is required and can\'t be empty'
                        },

                    }
                },


            }
        })
        .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow")
            $('#loginform').data('bootstrapValidator').resetForm();

            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serializeJSON(), function(result) {
                if(result['status'] == 'OK')
                    window.location.replace("/")
            }, 'json');
        });




});