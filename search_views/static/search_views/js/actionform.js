(function(){

  /**
  * Get the closest matching element up the DOM tree.
  * @private
  * @param  {Element} elem     Starting element
  * @param  {String}  selector Selector to match against
  * @return {Boolean|Element}  Returns null if not match found
  */
  var getClosest = function ( elem, selector ) {
    // Element.matches() polyfill
    if (!Element.prototype.matches) {
        Element.prototype.matches =
            Element.prototype.matchesSelector ||
            Element.prototype.mozMatchesSelector ||
            Element.prototype.msMatchesSelector ||
            Element.prototype.oMatchesSelector ||
            Element.prototype.webkitMatchesSelector ||
            function(s) {
                var matches = (this.document || this.ownerDocument).querySelectorAll(s),
                    i = matches.length;
                while (--i >= 0 && matches.item(i) !== this) {}
                return i > -1;
            };
    }

    // Get closest match
    for ( ; elem && elem !== document; elem = elem.parentNode ) {
        if ( elem.matches( selector ) ) return elem;
    }
    return null;

  };

  function addEventHandler(elem, eventType, handler) {
    if (elem.addEventListener)
        elem.addEventListener (eventType, handler, false);
    else if (elem.attachEvent)
        elem.attachEvent ('on' + eventType, handler);
  }

  function showField(field, globalFieldWrapper){
    var elm;
    if(globalFieldWrapper){
      elm = getClosest(field, globalFieldWrapper)
    } else {
      elm = field;
    }
    var oldDisplay = elm.getAttribute("data-display");
    elm.style.display = oldDisplay;
  }

  function hideField(field, globalFieldWrapper){
    var elm;
    if(globalFieldWrapper){
      elm = getClosest(field, globalFieldWrapper)
    } else {
      elm = field;
    }
    if(!elm.getAttribute("data-display")){
        elm.setAttribute("data-display", window.getComputedStyle(elm, null).getPropertyValue("display"));
    }
    elm.style.display = 'none';

    field.setAttribute("value", undefined);
    var opts = field.selectedOptions || [];
    for(var i = 0; i < opts.length; i++){
      opts[i].selected = false;
    }
  }

  document.addEventListener("DOMContentLoaded", prepareForm);

  function setVisibilities(target){
    var uuid = target.getAttribute("data-actionform")
    var actions = JSON.parse(target.getAttribute("data-action"));
    var globalFieldWrapper = target.getAttribute("data-field-wrapper");
    
    var value = target.value;
    var visibleItems = actions[value] || [];
    var allItems = document.querySelectorAll("[data-actionform='"+uuid+"']");
    allItems.forEach(function(item){
      var name = item.getAttribute("name");
      var isActions = !!item.getAttribute("data-action");
      var isSelection = !!item.getAttribute("data-selection");
      if(visibleItems.indexOf(name) !== -1 || isActions || isSelection){
        showField(item, globalFieldWrapper);
      } else {
        hideField(item, globalFieldWrapper);
      }
    });
  }

  function prepareForm(){
    var actions = document.querySelectorAll("[data-action]");
    actions.forEach(function(action){
      addEventHandler(action, "change", function(){return setVisibilities(event.target)});
      setVisibilities(action);
    });

  }

})();
