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

    var app = angular.module('my_account' , ['angular-bind-html-compile' , 'ngSanitize'] , function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}')
    }).config(function ($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

    var account_details = function ($scope , $http , $compile) {
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
                    $scope.customer_current_name = $scope.customer_name;
                    $scope.customer_current_phone = $scope.customer_phone;
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
        $scope.add_new_edit_address = function () {
            //TODO: Add param for address_name and pass it.
            //var param = 'address_name='+$scope.address_name;

            var onSuccess = function (response) {
                console.log(response.data);
                $scope.form_add_edit_address = response.data.form;
            };
            var onError = function (error) {
                console.log('Not working');
            };
            $http({
                method  : 'POST',
                url     : '/account/form/address/get',
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(onSuccess , onError);
        };
        $scope.process_address_add = function () {
            var param = "name="+$scope.name+"&address="+$scope.address
            +"&landmark="+$scope.landmark+"&city="+$scope.city+"&pincode="
            +$scope.pincode+"&phone="+$scope.phone+"&state="+$scope.state;

            var onSuccess = function (response) {
                console.log(response.data);
                $scope.status = response.data.status;
                $scope.error_message = response.data.error_message;
                $scope.form_add_edit_address = response.data.form;
                $scope.form_add_edit_address = null;
            };
            var onError = function (error) {
                console.log('Not working');
            };
            $http({
                method  : 'POST',
                url     : '/account/form/address/submit',
                data    :  param,
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(onSuccess , onError);
        };
        $scope.show_address_list = function () {
            var onSuccess = function (response) {
                console.log(response.data);
            };
            var onError = function (error) {
                console.log('Not working');
            };
            $http({
                method  : 'POST',
                url     : '/account/ajax/address/get'
            }).then(onSuccess , onError);
        }
    };
    app.controller('account_details' ,  account_details);
}());


