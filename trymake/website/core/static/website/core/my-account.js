/*
*   Author: Bineeth (bineeth@trymake.com)
*
*   Copyright (c) 2017 Sibibia Technologies Pvt Ltd
*   All Rights Reserved
*
*   Unauthorized copying of this file, via any medium is strictly prohibited
*   Proprietary and confidential
*/

(function () {

    var app = angular.module('my_account' , ['angular-bind-html-compile'] , function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}')
    }).config(function ($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

    var get_order = function ($scope , $http , $compile) {
        $scope.view_orders = function (get_list) {
            var url = 'ajax/orders/get';
            var onSuccess = function (responce) {
                $scope.return_list = responce.data;
            };
            var onReject = function () {
                $scope.return_list = "Something went worng.. Try again!"
            };
            $http.get(url,get_list).then(onSuccess , onReject);
        };
        $scope.update_profile_form = function () {
            var url = 'form/update/edit';
            //$window.location.href = url;
            var onSuccess = function (response) {
                $scope.form = response.data.form ;



                console.log($scope.form)
            };
            var onError = function (error) {
                $scope.form = "Oops..Something went worng! Sorrryyy!!"
            };
            $http.post(url).then(onSuccess , onError);

        };
        $scope.update_profile_submit = function () {
            var formData = "name="+$('input[name=name]').val()+
                    "&phone="+$('input[name=phone]').val();
            var onSuccess = function (responce) {
                $scope.status = responce.data.status;
                $scope.noError = responce.data.error_message;
                $scope.form = responce.data.form;
                if(responce.data.status === 'ok') {
                    $scope.name = $('input[name=name]').val();
                    $scope.phone = $('input[name=phone]').val();
                    $scope.form = null;
                }
                console.log(responce.data);
                console.log('Form' + $scope.form)
            };
            var onError = function (error) {
                $scope.status = "Error";
                console.log("Error")
            };
            $http({
                method  : 'POST',
                url     : 'form/update/submit',
                data    : formData,
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(onSuccess , onError);
        };

    };
    app.controller('get_order' ,  get_order);
}());


