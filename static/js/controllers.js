var app = angular.module('brochureApp', ['ngResource']);

app.factory('Products', ['$resource',
  function($resource){
    return $resource('phones/:phoneId.json', {}, {
      query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
    });
}]);

app.controller('brochureController', function ($scope) {
    $scope.products = [{first: 'Yan', last: 'Zheng', username: 'yanzheng'}, {first: 'Yan', last: 'Zheng', username: 'yanzheng'}, {first: 'Yan', last: 'Zheng', username: 'yanzheng'}, {first: 'Yan', last: 'Zheng', username: 'yanzheng'}];
    $scope.bestBuyClicked = function () {
        $scope.products = [{first: 'Xhacker', last: 'Liu', username: 'xhacker'}];
        $('#bestBuyList').addClass('active');
        $('#welcome').hide();
        $('#menubar').removeClass('hide');
        $('#table').removeClass('hide');
    };
});