/**
 * Created by ranganathan on 11/3/16.
 */

$(document).ready(function() {
    $('#studentform').bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },

            fields: {
                'student[FirstName]': {
                    validators: {
                        stringLength: {
                            min: 3,
                        },
                        notEmpty: {
                            message: 'Please supply your first name'
                        }
                    }
                },


                'student[LastName]': {
                    validators: {
                        stringLength: {
                            min: 2,
                        },
                        notEmpty: {
                            message: 'Please supply your last name'
                        }
                    }
                },
                'student[Email]': {
                    validators: {
                        notEmpty: {
                            message: 'Please supply your email address'
                        },
                        emailAddress: {
                            message: 'Please supply a valid email address'
                        }
                    }
                },
                'student[Phone]': {
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
                'student[LocalAddressLine1]': {
                    validators: {
                        stringLength: {
                            min: 8,
                        },
                        notEmpty: {
                            message: 'Please supply your street address'
                        }
                    }
                },
                'student[LocalAddressCity]': {
                    validators: {
                        stringLength: {
                            min: 4,
                        },
                        notEmpty: {
                            message: 'Please supply your city'
                        }
                    }
                },
                'student[LocalAddressState]': {
                    validators: {
                        notEmpty: {
                            message: 'Please select your state'
                        }
                    }
                },
                'student[LocalAddressZip]': {
                    validators: {
                        notEmpty: {
                            message: 'Please supply your zip code'
                        },
                        zipCode: {
                            country: 'US',
                            message: 'Please supply a vaild zip code'
                        }
                    }
                },
                'student[PrimaryMajor]': {
                    validators: {
                        notEmpty: {
                            message: 'Please select your state'
                        }
                    }
                },

                'student[Race][]': {
                    validators: {
                        choice: {
                            min: 1,
                            max: 3,
                            message: 'Please choose a option'
                        }
                    }
                },





            }
        })
        .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
            $('#studentform').data('bootstrapValidator').resetForm();

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

            /*
                 Function to carry out the actual POST request to S3 using the signed request from the Python app.
                 */
                function uploadFile(file, s3Data, url, file2, s3Data2, url2){
                    const xhr = new XMLHttpRequest();
                    xhr.open('POST', s3Data.url);
                    xhr.setRequestHeader('x-amz-acl', 'public-read');




                    const postData = new FormData();
                    for(key in s3Data.fields){
                        postData.append(key, s3Data.fields[key]);
                    }
                    postData.append('file', file);


                    xhr.onreadystatechange = () => {
                        if(xhr.readyState === 4){
                            if(xhr.status === 200 || xhr.status === 204){
                                document.getElementById('preview').src = url;
                                document.getElementById('avatar-url').value = url;
                            }
                            else{
                                alert('Could not upload file.');
                            }
                        }
                    };

                    xhr.send(postData);

                    const xhr2 = new XMLHttpRequest();
                    xhr2.open('POST', s3Data2.url);
                    xhr2.setRequestHeader('x-amz-acl', 'public-read');

                    const postData2 = new FormData();
                    for(key in s3Data2.fields){
                        postData2.append(key, s3Data2.fields[key]);
                    }
                    postData2.append('file', file2);

                    xhr2.onreadystatechange = () => {
                        if(xhr2.readyState === 4){
                            if(xhr2.status === 200 || xhr2.status === 204){
                                document.getElementById('preview').src = url2;
                                document.getElementById('avatar-url').value = url2;
                            }
             
                        }
                    };

                    xhr2.send(postData2);


                }

            /*
             Function to get the temporary signed request from the Python app.
             If request successful, continue to upload the file using this signed
             request.
             */
            function getSignedRequest(file,value,file2, value2){
                const xhr = new XMLHttpRequest();
                xhr.open('GET', `/sign-s3?file-name=${file.name}&file-type=${file.type}&file-value=${value}&file-name2=${file2.name}&file-type2=${file2.type}&file-value2=${value2}`);
                xhr.onreadystatechange = () => {
                    if(xhr.readyState === 4){
                        if(xhr.status === 200){
                            const response = JSON.parse(xhr.responseText);
                            uploadFile(file, response.data1, response.url1, file2, response.data2, response.url2);
                        }
                    
                    }
                };
                xhr.send();
            }

            /*
             Function called when file input updated. If there is a file selected, then
             start upload procedure by asking for a signed request from the app.
             */
            function initUpload(){
                const resumeFile = document.getElementById('file-input').files;
                const coverFile = document.getElementById('file-input1').files;

                const file = resumeFile[0];
                const file2 = coverFile[0];
                if(!file){
                    return alert('No file selected.');
                }
                getSignedRequest(file,'Resume', file2,'CoverLetter');
            }

            function coverLetterUpload(){
                const files = document.getElementById('file-input1').files;
                const file = files[0];
                if(!file){
                    return alert('No file selected.');
                }
                getSignedRequest(file,'Cover');
            }

            /*
             Bind listeners when the page loads.
             */
            (() => {
                initUpload();
                //coverLetterUpload();
            })();

        });


});

