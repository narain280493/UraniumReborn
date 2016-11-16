/**
 * Created by ranganathan on 11/3/16.
 */

$(document).ready(function() {

    $('#facultyform').bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },

            fields: {
                'faculty[FirstName]': {
                    validators: {
                        stringLength: {
                            min: 3,
                        },
                        notEmpty: {
                            message: 'Please supply your first name'
                        }
                    }
                },
                'faculty[LastName]': {
                    validators: {
                        stringLength: {
                            min: 3,
                        },
                        notEmpty: {
                            message: 'Please supply your last name'
                        }
                    }
                },
                'faculty[Email]': {
                    validators: {
                        notEmpty: {
                            message: 'Please supply your email address'
                        },
                        emailAddress: {
                            message: 'Please supply a valid email address'
                        }
                    }
                },
                'faculty[Phone]': {
                    validators: {
                        notEmpty: {
                            message: 'Please supply your phone number'
                        },
                        phone: {
                            country: 'US',
                            message: 'Please supply a vaild phone number with area code'
                        }
                    }
                },

                'faculty[Department]': {
                    validators: {
                        notEmpty: {
                            message: 'Please select the department'
                        }
                    }
                },

                'secondFaculty[FirstName]': {
                    validators: {
                        stringLength: {
                            min: 2,
                        },

                    }
                },
                'secondFaculty[LastName]': {
                    validators: {
                        stringLength: {
                            min: 2,
                        },

                    }
                },
                'secondFaculty[Email]': {
                    validators: {

                        emailAddress: {
                            message: 'Please supply a valid email address'
                        }
                    }
                },
                'secondFaculty[Phone]': {
                    validators: {
                        phone: {
                            country: 'US',
                            message: 'Please supply a vaild phone number with area code'
                        }
                    }
                },

                'secondFaculty[Department]': {
                    validators: {

                    }
                },

                'gradStudent[FirstName]': {
                    validators: {
                        stringLength: {
                            min: 2,
                        },

                    }
                },
                'gradStudent[LastName]': {
                    validators: {
                        stringLength: {
                            min: 2,
                        },

                    }
                },
                'gradStudent[Email]': {
                    validators: {

                        emailAddress: {
                            message: 'Please supply a valid email address'
                        }
                    }
                },
                'gradStudent[Phone]': {
                    validators: {

                        phone: {
                            country: 'US',
                            message: 'Please supply a vaild phone number with area code'
                        }
                    }
                },
                'gradStudent[Department]': {
                    validators: {

                    }
                },


                'apprenticeship[Title]': {
                    validators: {
                        stringLength: {

                            min:2,
                            max: 80,
                        },
                        notEmpty: {
                            message: 'Please supply your Apprenticeship Title'
                        }
                    }
                },


                'apprenticeship[Description]': {
                    validators: {
                        stringLength: {

                            min:2,
                            max: 1200,
                        },
                        notEmpty: {
                            message: 'Please supply your Apprenticeship Description'
                        }
                    }
                },


                'apprenticeship[fieldOfStudy][]': {
                    validators: {
                        choice: {
                            min: 1,
                            message: 'Please choose a option'
                        }
                    }
                },


                'apprenticeship[Weblink]': {
                    validators: {
                        uri: {
                            message: 'The entered URL is not valid'
                        }
                    }
                }
            }
        })
        .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow")
            $('#facultyform').data('bootstrapValidator').resetForm();

            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serializeJSON(), function(result) {
                console.log(result);
            }, 'json');
        });







});