/**
 * Created by Bineeth on 30-06-2017.
 */

(function(){

    var app = angular.module('login', []).config(function ($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    var loginEmail = function ($scope, $http) {
        $scope.check_mail = function (email) {
            var param = {
                'email' : email
            };

            var onSuccess = function (responce) {
                $scope.user = responce.data;
            };
            var onReject = function (error) {
                $scope.error = "no email exists";
            };
            $http.post('/check_account' , param)
                .then(onSuccess , onReject);
        };

        $scope.login = function (email , password) {
            var param = {
                'email' : email,
                'password' : password
            };
            var onSuccess = function (response) {
                $scope.msg = "successfully logged in";
            };
            var onReject = function (error) {
                $scope.error = "Incorrect password";
            };
            $http.post('/login' , param)
                .then(onSuccess , onReject);
        }

    };
    app.controller('loginEmail' ,  loginEmail);

}());