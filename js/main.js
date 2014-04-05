MLBTrack = Backbone.Model.extend({});

MLBTrackCollection = Backbone.Collection.extend({
  model: MLBTrack,

  url: 'js/mlb-tracks-combined.json',

  getTeam: function(teamAbbr) {
    return this.where({
      team_abbr: teamAbbr.toUpperCase()
    });
  }
})

MLBTrackView = Backbone.View.extend({
  tag: 'li',

  className: 'media',

  events: {
    'click button': "playTrack"
  },

  template: _.template($('#rdio-track-template').html()),

  canPlay: function() {
    var rdioKeys = this.model.get('rdio_keys');
    return rdioKeys.length > 0;
  },

  playTrack: function() {
    if (this.canPlay()) {
      R.player.play({
        source: this.model.get('rdio_keys')[0]
      })
    }
  },

  render: function() {
    this.$el.html(this.template(this.model.attributes));
    if (!this.canPlay()) {
      this.$el.find('button').addClass('disabled');
    }
    return this;
  }
});

MLBTrackListView = Backbone.View.extend({
  el: '#track-list',

  collection: null,

  initialize: function(options) {
    this.options = options;
    this.listenTo(this.collection, 'add', this.addOne);
    this.listenTo(this.collection, 'reset', this.render);

  },

  addOne: function(track, collection, options) {
    if (track.get('team_abbr') != this.options.activeTeam) {
      return;
    }

    var trackView = new MLBTrackView({
      model: track
    })
    this.$el.prepend(trackView.render().el);
  },

  render: function() {
    var that = this;

    this.$el.empty();
    this.collection.each(function(track) {
      if (track.get('team_abbr') != that.options.activeTeam) {
        return;
      }

      var trackView = new MLBTrackView({
        model: track
      })
      that.$el.prepend(trackView.render().el);
    })
  }

})

TeamSelectView = Backbone.View.extend({
  el: '#team-select',

  events: {
    'click button': 'selectTeam'
  },

  selectTeam: function(e) {
    var teamAbbr = $(e.target).text();
    console.log(trackListView.options.activeTeam, teamAbbr);
    trackListView.options.activeTeam = teamAbbr;
    trackListView.render();
  }
});

var trackCollection = new MLBTrackCollection();

var trackListView = new MLBTrackListView({
  collection: trackCollection,
  activeTeam: 'LAD'
});
trackCollection.fetch();

var teamSelectView = new TeamSelectView({
  trackListView: trackListView
});

var main = function() {
  if (!rdioUtils.startupChecks()) {
    return;
  }

  R.ready(function() {
    rdioUtils.authWidget($('#authenticate'));
  });
}

main();
