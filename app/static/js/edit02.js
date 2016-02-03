/**
 * Created by Administrator on 11/18/2015.
 */
$('#my-editable').editable({
    touch : true, // Whether or not to support touch (default true)
    lineBreaks : true, // Whether or not to convert \n to <br /> (default true)
    toggleFontSize : true, // Whether or not it should be possible to change font size (default true),
    closeOnEnter : false, // Whether or not pressing the enter key should close the editor (default false)
    event : 'click', // The event that triggers the editor (default dblclick)
    tinyMCE : false, // Integrate with tinyMCE by settings this option to true or an object containing your tinyMCE configuration
    emptyMessage : '<em>Please write something.</em>', // HTML that will be added to the editable element in case it gets empty (default false)
    callback : function( data ) {
        // Callback that will be called once the editor is blurred
        if( data.content ) {
            // Content has changed...
        }
        if( data.fontSize ) {
            // the font size has changed
        }

        // data.$el gives you a reference to the element that was edited
        data.$el.effect('blink');
    }
});
