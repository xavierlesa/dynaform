/*
 * related fields
 */

(function($){

    $("*[data-related-field]").each(function(){
    
        var options = $(this).attr('data-related-field-options') || {};
        if(options){
            options = options.split(';');
            var r = {};
            options.forEach(function(a){ 
                var b = a.trim().split(':'); 
                r[b[0]] = (b[1]||'').trim();
                return r
            });
        }

        options = $.extend({}, r);

        var related_field = $(this);
        var ids = options.ids.split(/\s*,\s*/);
        var action = options.action.split('/');

        $("#"+ids.join(", #")).on('change', function(){

            var id = $("option:selected()", this).val();
            action.pop();
            action.push(id);
            var xhr = $.getJSON(action.join('/')+'/');

            xhr.done(function(data, textStatus, jqXHR){
                // elimina los anteriores menos el primero
                $('option', related_field).not(':nth(0)').remove();
                // carga los nuevos
                $.each(data.data, function(i, value){
                    related_field.append($('<option>').text(value[1]).attr('value', value[0]));
                });
            });

        });

    });

})(jQuery);
