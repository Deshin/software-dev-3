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

requirejs(['jquery', 'knockout', 'kopunches', 'kofilebind', 'pager', 'jqueryvalidate', 'bootbox', 'bootstrap', 'crypto.SHA'], function($, ko, kopunches, kofilebind, pager, $valid, bootbox, bootstrap, crypt) {
  function RootViewModel() {
    var self = this;
    self.search = ko.observable("");
    self.loginState = ko.observable('UnregisteredUser');

    self.onSearchClick = function() {
      if (self.search() === "") {
        window.location.assign("/");
      } else {
        window.location.assign("/#!/publications?search="+encodeURIComponent(self.search()));
      }
    };
    self.loginModal = function() {
      bootbox.dialog({
        message: '<form id="loginModal"></form>',
        title: "Custom title",
        show: true,
        backdrop: true,
        closeButton: true,
        animate: true,
        className: "my-modal",
        buttons: {
          "Confirm": {
            className: "btn-success",
            callback: loginUser
          },
          "Cancel": {
            className: "btn-danger"
          }
        }
      });
      $('#loginModal').load('views/loginModal.html');
    };
    self.logout = function() {
      self.loginState('UnregisteredUser');
    };
    self.getVM = function(path) {
      return function(callback) {
        requirejs(['/js/ko/viewmodels/'+path+'.js'], function(mod) {
          callback(mod);
        });
      };
    };
  }

  rootViewModel = new RootViewModel();

  pager.Href.hash = '#!/';

  pager.extendWithPage(rootViewModel);

  ko.punches.enableAll();

  ko.applyBindings(rootViewModel);

  pager.start();

  function loginUser(result) {
    var username = $('#username').val();
    var password = CryptoJS.SHA256($('#password').val());
    if(username && password) {

      var loginObject = {
        username: username,
        hash: password.toString()
      };

      // $.ajax({
      //   url: "/api/login.py",
      //   type: "POST",
      //   contentType: "application/json",
      //   data: JSON.stringify(loginObject),
      //
      //   success: function(data) {
      //     rootViewModel.loginState('RegisteredUser');
      //   },
      //
      //   error: function (jqXHR) {
      //     console.log("Error: " + jqXHR.status + " - " + jqXHR.statusText);
      //   },
      // });
      rootViewModel.loginState('RegisteredUser');
    }

  }
});
