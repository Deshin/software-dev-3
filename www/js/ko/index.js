/**
* Configure require.js, this will load all view models for the
* individual partials.
*
* @requires require.js
*/
requirejs.config({
  baseUrl: 'js',
  urlArgs: "bust=" + (new Date()).getTime(),
  paths: {
    jquery: 'jquery-2.1.3.min',
    jqueryvalidate: 'jquery.validate.min',
    knockout: 'knockout-3.3.0',
    kopunches: 'knockout.punches.min',
    kofilebind: 'knockout-file-bindings',
    pager: 'pager.min',
    bootbox: 'bootbox.min',
    bootstrap: 'bootstrap.min',
    crypto: 'crypto.core',
    'crypto.SHA': 'sha256'
  },
  shim: {
    'crypto.SHA' : ['crypto']
  }
});

/**
* The index.js view model is loaded with index.html,
* this view model will initialize require and the functions of the
* root page (login, admin functions, etc).
*
* @requires jQuery
* @requires knockout.js
* @requires knockout.punches
* @requires knockout.filebind
* @requires pager.js
* @requires jQuery.validate
* @requires bootbox
* @requires bootstrap
* @requires CryptoJS
*
* @author Deshin
* @author Anthony
*/
requirejs(['jquery', 'knockout', 'kopunches', 'kofilebind', 'pager', 'jqueryvalidate', 'bootbox', 'bootstrap', 'crypto.SHA'], function($, ko, kopunches, kofilebind, pager, $valid, bootbox, bootstrap, crypt) {
  function RootViewModel() {
    var self = this;
    self.search = ko.observable("");
    self.loginState = ko.observable('unregistered');
    self.loginUsername = ko.observable("");
    self.accreditationUrl = ko.observable('/#!/publications?search='+JSON.stringify([{
      field: 'Accreditation',
      value: 'Accredited',
      operator: 'equals'
    }]));

    /**
    * @method onSearchClick
    * Build the search string when the search button is clicked.
    */
    self.onSearchClick = function() {
      if (self.search() === "") {
        window.location.assign("/#!/");
      } else {
        window.location.assign("/#!/publications?search="+encodeURIComponent(self.search()));
      }
    };
    /**
    * @method loginModal
    * Create the login frame that appears as a modal on the page,
    * the modal requests username and password which is then checked with
    * the endpoint for validation.
    * @callback loginUser
    * The loginUser callback will login the user when the modal closes
    */
    self.loginModal = function() {
      bootbox.dialog({
        message: '<form id="loginModal" submit="" data-bind="submit: loginUser"></form>',
        title: "Login",
        show: true,
        backdrop: true,
        closeButton: true,
        animate: true,
        className: "my-modal",
        buttons: {
          success: {
            label: "Login",
            className: "btn-success",
            callback: loginUser
          },
          danger: {
            label: "Cancel",
            className: "btn-danger"
          }
        }
      });
      $('#loginModal').load('views/loginModal.html');
    };
    /**
    * @method logout
    * Logout the current user and redirect to the home page (and refresh).
    */
    self.logout = function() {
      self.loginState('unregistered');
      window.location.assign("/");
    };
    /**
    * @method getVM
    * The getVM function will get the view model for a partial html page,
    * required by pager for lazy MVVM binding.
    */
    self.getVM = function(path) {
      return function(callback) {
        requirejs(['/js/ko/viewmodels/'+path+'.js'], function(mod) {
          callback(mod);
        });
      };
    };
  }

  /**
  * @global rootViewModel
  * The rootViewModel is accessable from any view model for checking
  * authorization level and credentials.
  */
  rootViewModel = new RootViewModel();

  pager.Href.hash = '#!/';

  pager.extendWithPage(rootViewModel);

  ko.punches.enableAll();

  ko.applyBindings(rootViewModel);

  pager.start();

  /**
  * @method loginUser
  * This method will grab the username and password from the modal and
  * use them in an AJAX request to the login endpoint to check if the user
  * is authorized. The password is hashed before sending.
  * @requires jQuery
  */
  function loginUser(result) {
    var username = $('#username').val();
    var password = CryptoJS.SHA256($('#password').val());
    if(username && password) {

      var loginObject = {
        username: username,
        hash: password.toString()
      };

      $.get('/api/login.py', loginObject)
      .done(function(data) {
        rootViewModel.loginState(data.Permission);
        rootViewModel.loginUsername(username);
      })
      .error(function (jqXHR) {
        rootViewModel.loginState('unregistered');
        bootbox.dialog({
          message: "Error (" + jqXHR.status + ") " + jqXHR.statusText,
          title: "Error Uploading",
          buttons: {
            'OK': {
              className: "btn-success"
            }
          }});
        });
      }

    }
  });
