/*
 * Auto-attach ajax for forms
 *
 * usage:
 *
 */

$(function(){

    $("form[data-ajaxsend]").each(function(){

        var options = $(this).attr('data-ajaxsend-options') || {};
        if(options){
            options = options.split(';');
            var r = {};
            options.forEach(function(a){ 
                var b = a.trim().split(':'); 
                r[b[0]] = (b[1]||'').trim();
                return r
            });
        }

        options = $.extend({
            done_element: this,
            done_event: 'done',
            fail_element: this,
            fail_event: 'fail',
            //complete_element: this,
            //complete_event: 'complete',
            sending_element: this,
            sending_event: 'sending',
            beforesend_element: this,
            beforesend_event: 'beforesend',
            loading_img: '/statics/img/loading.gif'
        }, r);

        var i = new Image();
        i.src = decodeURIComponent(options.loading_img);

        $(this).append($($("<div class='loading' style='text-align:center' />").append(i)).hide());

        function disabled(form){
            form.find('input,textarea,select').attr('disabled', true);
        }

        function enabled(form){
            form.find('input,textarea,select').attr('disabled', false);
        }

        $(this).on('submit', function(event){
            event.preventDefault();
            var $form = $(this);
            var formData = $form.serialize();

            /* si hay un file entre los campos usa el otro metodo */
            var filesInput = $form.find('input[type=file]');

            if(filesInput.length){

                // Create a new FormData object.
                formData = new FormData();

                for (var f = 0; f < filesInput.length; f++) {

                    // Loop through each of the selected files.
                    for (var i = 0; i < filesInput[f].files.length; i++) {
                      var file = filesInput[f].files[i];

                      // Add the file to the request.
                      formData.append(filesInput[f].name, file, file.name);
                    }
                }

                var formDataString = $form.serializeArray();
                
                for (var i = 0; i < formDataString.length; i++) {
                    formData.append(formDataString[i].name, formDataString[i].value);
                }
            }

            var xhr = $.ajax({
                type: 'POST',
                url: $form.attr('action'),
                data: formData,
                dataType: 'json',
                global: false,
                cache: false,
                contentType: false,
                processData: false,
                beforeSend: function(jqXHR){
                    $form.find('.loading').show();
                    disabled($form);
                    console.log('loading...');
                    $(options.beforesend_element).trigger(options.beforesend_event, jqXHR);
                }
            });

            xhr.always(function(response){
                $form.find('.loading').hide();
                console.log('stop');
                enabled($form);
                $(options.sending_element).trigger(options.sending_event, response);
            });

            xhr.done(function(data, textStatus, jqXHR){
                $(options.done_element).trigger(options.done_event, {data:data, textStatus:textStatus, jqXHR:jqXHR});
            });

            xhr.fail(function(jqXHR, textStatus, errorThrown){
                $(options.fail_element, $form).trigger(options.fail_event, {jqXHR:jqXHR, textStatus:textStatus, errorThrown:errorThrown});
                try {
                    $.each(jqXHR.responseJSON.errors, function(key, val){
                        $form
                            .find("*[name="+key+"]")
                            .addClass('error')
                            .next('.error')
                            .css('display', 'block')
                            .text(val[0]);
                    });
                } catch(E){};
            });

            return false;
        });
    });

});
