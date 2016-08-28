(function(){
  var app = angular.module('search',[]);
  app.controller("QueryController", ["$scope", "$http", function($scope, $http){
    this.query = {};
    this.response = [];
    this.noTest = false;
    this.loading = false;
    this.courseEntered = false;
    this.semestersEntered = false;
    this.testsEntered = false;
    this.semesters = [];
    this.exams = [];
    this.showTable = false;

    this.checkNoTest = function(){
      for (i = 0; i < this.response.length; i += 1) {
        if (this.response[i].empty){
          continue;
        }
        return false;
      }
      return true;
    };

    this.send = function(queryCtrl){
      this.response = [];
      this.showTable = true;
      this.loading = true;
      this.noTest = false;
      $http({
        url: "/search/",
        method: "GET",
        params: queryCtrl.query
      }).then(function(res){
        queryCtrl.loading = false;
        queryCtrl.response = res.data.list;
        if (queryCtrl.checkNoTest()) {
          queryCtrl.noTest = true;
        } else {
          queryCtrl.noTest = false;
        }
      }, function(res){
        queryCtrl.loading = false;
        queryCtrl.noTest = true;
      });
    };

    this.toggleCourse = function(queryCtrl) {
      this.course = queryCtrl.query.course
      this.courseEntered = false;
      if (this.course != "? undefined:undefined ?") {
        $http({
          url: "/getSemesters",
          method: "GET",
          params: {
            course: this.course.replace(/ /g, '')
          }
        }).then(function(res){
            queryCtrl.semesters = res.data.semesters;
            queryCtrl.courseEntered = true;
        })
      }
    }

    this.toggleSemester = function(queryCtrl) {
      if (this.course == "? undefined:undefined ?") {
        this.semestersEntered = false;
      } else {
        this.semestersEntered = true;
      }
    }

    this.toggleTest = function(queryCtrl) {
      this.exams = queryCtrl.query.test
      if (this.course == "? undefined:undefined ?") {
        this.testsEntered = false;
      } else {
        this.testsEntered = true;
      }
    }
  }]);
})();
