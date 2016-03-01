/*
 * Auto-attach ajax for forms
 *
 * <form action="..." method="post" data-ajaxsend data-options="...">
 * ...
 * <input type="submit" name="submit" value="Send" />
 * </form>
 *
 */

$(function(){

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }


    $("form[data-ajaxsend]").each(function(){

        var options = $(this).attr('data-ajaxsend-options') || "";
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
            loading_img: 'http://s11.postimg.org/lb6hylp9r/loading.gif'
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

        // capture submit
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
                //contentType: false, /* bug? no termina de procesar los datos la vista de django y POST viaja vacio */
                processData: false,
                beforeSend: function(jqXHR, settings){
                    $form.find('.loading').show();
                    disabled($form);
                    console.log('loading...');
                    $(options.beforesend_element).trigger(options.beforesend_event, jqXHR);

                    // CSRFToken protect
                    if (csrftoken && !csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        jqXHR.setRequestHeader("X-CSRFToken", csrftoken);
                    }
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
                $form.trigger('reset'); // clean
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
        
        // tracking para google analytics
        // on submit
        $(this).on('done', function(event){
            var $form = $(this);
            var action = $form.attr('action') + '/submited/';
            var custom_tarck_pageview = $form.data('track_pageview');
            var track_pageview = action || custom_tarck_pageview;

            if(window._gaq){
                _gaq.push(['_trackPageview', track_pageview]);
            } else if(window.ga) {
                ga('send', 'pageview', track_pageview);
            }
        });
    });

    /* Tracking para campos de formularios DEPRECADO -> hotjar */
    /*
    if (window.ga || window._gaq) {
      $("form").each(function() {
        var $form = $(this);

        var formName = $(this).attr('name') || $(this).attr('id');
        
        $('input, textarea, select', $form).on('blur', function() {
          var fieldName = $(this).attr('name');
          if(window._gaq){
            _gaq.push(['_trackEvent', formName, 'completed', fieldName]);
          } else if(window.ga) {
            ga('send', 'event', formName, 'completed', fieldName);
          }
        });
      });
    }
    */
});
