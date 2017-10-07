Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base

<TestFixture()> _
Public Class BasePlayerTests

    Public Property PlayerSeason As BasePlayerSeason
    Public Property StatFunctions As BasePlayerStatisticalFunctions
    Public Property Stats As Dictionary(Of String, Object)
    Public Property pts1 As Dictionary(Of String, Object)
    Public Property Year As Integer

    <SetUp()> _
    Public Sub SetUp()
        Me.PlayerSeason = New BasePlayerSeason()
        Me.pts1 = New Dictionary(Of String, Object) From {
                    {"Minutes", 1100},
                    {"Games", 40},
                    {"Points", 1100},
                    {"Rebounds", 40}
                }
        Me.Year = 2010
    End Sub

    <TearDown()> _
    Public Sub TearDown()
        'nothing to go here
    End Sub

    ' start tests

    <Test()> _
    Public Sub New_NoParameter_ReturnsTrue()
        Dim player As New BasePlayer
        Assert.IsFalse(player Is Nothing, "Player constructor failed")
    End Sub

    <Test()> _
    Public Sub AddId_ValidId_ReturnsTrue()
        Dim player As New BasePlayer
        Dim id As BasePlayerId = Me.CreateId
        player.AddId(id)
        Assert.IsFalse(player Is Nothing, "Player constructor failed")
        Assert.AreEqual(player.Ids(0), id, "Ids are not the same")
    End Sub

    <Test()> _
    Public Sub AddIds_ValidIds_ReturnsTrue()
        Dim player As New BasePlayer
        Dim ids As List(Of BasePlayerId) = Me.CreateIds
        player.AddIds(ids)
        Assert.IsFalse(player Is Nothing, "Player constructor failed")
        Assert.AreEqual(player.Ids(0), ids(0), "Ids are not the same")
        Assert.AreEqual(player.Ids(1), ids(1), "Ids are not the same")
    End Sub

    <Test()> _
    Public Sub AddSeason_ValidParameter_ReturnsTrue()
        Dim player As New BasePlayer
        Dim season As BasePlayerSeason = Me.CreateSeason(2010)
        player.AddSeason(season)
        Assert.AreEqual(player.Seasons(0), season, "Seasons are not the same")
    End Sub

    <Test()> _
    Public Sub AddSeasons_ValidParameter_ReturnsTrue()
        Dim player As New BasePlayer
        Dim seasons As List(Of BasePlayerSeason) = Me.CreateSeasons
        player.AddSeasons(seasons)
        Assert.AreEqual(player.Seasons, seasons, "Seasons are not the same")
    End Sub

    <Test()> _
    Public Sub CareerTotal_ValidStatname_ReturnsTrue()
        Dim player As New BasePlayer
        player.AddSeason(Me.CreateSeasonWithStats(2010))
        Dim ct As Double = player.CareerTotal("Points")
        Assert.AreEqual(CDbl(Me.pts1.Item("Points")) * 2, ct, "Points are not equal")
    End Sub

    <Test()> _
    Public Sub GetCareer_NoParameter_ReturnsTrue()
        Dim player As New BasePlayer
        player.Seasons = New List(Of BasePlayerSeason)
        Dim year As Integer = 2010
        Dim seasons As List(Of BasePlayerSeason) = Me.CreateSeasonsWithStats()
        player.AddSeasons(seasons)
        Dim getCareer As List(Of BasePlayerSeason) = player.GetCareer()
        Assert.AreEqual(getCareer(0), seasons(0), "Seasons 1 are not equal.")
        Assert.AreEqual(getCareer(1), seasons(1), "Seasons 2 are not equal.")
    End Sub

    <Test()> _
    Public Sub GetIds_NoParameter_ReturnsTrue()
        Dim player As New BasePlayer
        Dim createdIds As List(Of BasePlayerId) = Me.CreateIds
        player.AddIds(createdIds)
        Assert.AreEqual(2, createdIds.Count, "Count of created IDs is not 2")
        Dim gotIdStrings As List(Of String) = player.GetIdStrings()
        Assert.AreEqual("ABDULKA01", gotIdStrings(0), "Id String 1 not the same.")
        Assert.AreEqual("ALLENRA01", gotIdStrings(1), "Id String 2 not the same.")
    End Sub

    <Test()> _
    Public Sub GetSources_NoParameter_ReturnsTrue()
        Dim player As New BasePlayer
        Dim source As String = "basketball-reference.com"
        Dim createdIds As List(Of BasePlayerId) = Me.CreateIds
        player.AddIds(createdIds)
        Assert.AreEqual(2, createdIds.Count, "Count of created IDs is not 2")
        Dim gotSourceStrings As List(Of String) = player.GetSources
        Assert.AreEqual(source, gotSourceStrings(0), "Source String 1 not the same.")
        Assert.AreEqual(source, gotSourceStrings(1), "Source String 2 not the same.")
    End Sub

    <Test()> _
    Public Sub GetIdsAndSources_NoParameter_ReturnsTrue()
        Dim player As New BasePlayer
        Dim source As String = "basketball-reference.com"
        Dim createdIds As List(Of BasePlayerId) = Me.CreateIds
        player.AddIds(createdIds)
        Assert.AreEqual(2, createdIds.Count, "Count of created IDs is not 2")
        Dim sids As Dictionary(Of String, String) = player.GetIdsAndSources
        Assert.AreEqual("ABDULKA01", sids.Keys(0), "Id String 1 not the same.")
        Assert.AreEqual("ALLENRA01", sids.Keys(1), "Id String 1 not the same.")
        Assert.AreEqual(source, sids.Values(0), "Source String 1 not the same.")
        Assert.AreEqual(source, sids.Values(1), "Source String 2 not the same.")
    End Sub

    <Test()> _
    Public Sub GetSeason_ValidSeason_ReturnsTrue()
        Dim player As New BasePlayer
        Dim year As Integer = 2010
        player.AddSeason(Me.CreateSeason(year))
        Dim season As BasePlayerSeason = player.GetSeason(player.Seasons, year)
        Assert.AreEqual(player.Seasons(0), season, "Seasons are not equal.")
        Assert.AreEqual(season.Year, year, "Years are not equal.")
    End Sub

    <Test()> _
    Public Sub GetSeasons_ValidSeasonRange_ReturnsTrue()
        Dim player As New BasePlayer
        player.Seasons = New List(Of BasePlayerSeason)
        Dim seasons As List(Of BasePlayerSeason) = Me.CreateSeasonsWithStats()
        player.AddSeasons(seasons)
        Dim gottenSeasons As List(Of BasePlayerSeason) = player.GetSeasons(Me.Year - 1, Me.Year)
        Assert.AreEqual(player.Seasons.Count, gottenSeasons.Count, "Season counts are not equal.")
        Assert.AreEqual(gottenSeasons(0), player.Seasons(0), "Seasons 1 are not equal.")
        Assert.AreEqual(gottenSeasons(1), player.Seasons(1), "Seasons 2 are not equal.")
    End Sub

    <Test()> _
    Public Sub GetSeasons_PassSeasonsListAndValidSeasonRange_ReturnsTrue()
        Dim player As New BasePlayer
        player.Seasons = New List(Of BasePlayerSeason)
        Dim seasons As List(Of BasePlayerSeason) = Me.CreateSeasonsWithStats()
        player.AddSeasons(seasons)
        Dim gottenSeasons As List(Of BasePlayerSeason) = player.GetSeasons(player.GetCareer, Me.Year - 1, Me.Year)
        Assert.AreEqual(player.Seasons.Count, gottenSeasons.Count, "Season counts are not equal.")
        Assert.AreEqual(gottenSeasons(0), player.Seasons(0), "Seasons 1 are not equal.")
        Assert.AreEqual(gottenSeasons(1), player.Seasons(1), "Seasons 2 are not equal.")
    End Sub

    <Test()> _
    Public Sub LastSeason_NoParameters_ReturnsTrue()
        Dim player As New BasePlayer
        player.Seasons = New List(Of BasePlayerSeason)
        Dim seasons As List(Of BasePlayerSeason) = Me.CreateSeasonsWithStats()
        player.AddSeasons(seasons)
        Dim ls As BasePlayerSeason = player.LastSeason
        Assert.AreEqual(ls, player.Seasons(player.Seasons.Count - 1), "Seasons 1 are not equal.")
    End Sub

    <Test()> _
    Public Sub SeasonRangeTotal_ValidParameter_ReturnsTrue()
        Dim player As New BasePlayer
        player.AddSeasons(Me.CreateSeasonsWithStats)
        Dim totalPoints As Double = player.SeasonRangeTotal(player.Seasons, "Points", Me.Year - 1, Me.Year)
        Dim pts1TotalPoints As Double = (CDbl(pts1("Points")) + CDbl(pts1("Points"))) * 2
        Assert.AreEqual(pts1TotalPoints, totalPoints, "total points not equal")
    End Sub

    <Test()> _
    Public Sub SeasonTotal_ValidParameter_ReturnsTrue()
        Dim player As New BasePlayer
        player.AddSeasons(Me.CreateSeasonsWithStats)
        Dim totalPoints As Double = player.GetSeasonTotal("Points", Me.Year)
        Dim pts1TotalPoints As Double = (CDbl(pts1("Points")) + CDbl(pts1("Points")))
        Assert.AreEqual(pts1TotalPoints, totalPoints, "total points not equal")
    End Sub

    ' helper functions
    Private Function CreateId() As BasePlayerId
        Return New BasePlayerId("ABDULKA01", "basketball-reference.com")
    End Function

    Private Function CreateIds() As List(Of BasePlayerId)
        Return New List(Of BasePlayerId) From {
            {New BasePlayerId("ABDULKA01", "basketball-reference.com")},
            {New BasePlayerId("ALLENRA01", "basketball-reference.com")}
        }
    End Function

    Private Function CreateSeason(ByVal year As Integer) As BasePlayerSeason
        Dim season As New BasePlayerSeason(year)
        Return season
    End Function

    Private Function CreateSeasonWithStats(ByVal year As Integer) As BasePlayerSeason
        Dim season As New BasePlayerSeason(year)
        Dim teamSeasons As New List(Of BasePlayerTeamSeason) From {
            {New BasePlayerTeamSeason(year, Me.pts1)},
            {New BasePlayerTeamSeason(year, Me.pts1)}
        }
        season.AddPlayerTeamSeasons(teamSeasons)
        Return season
    End Function

    Private Function CreateSeasons() As List(Of BasePlayerSeason)
        Dim season As New List(Of BasePlayerSeason)
        Return season
    End Function

    Private Function CreateSeasonsWithStats() As List(Of BasePlayerSeason)
        Dim seasons As New List(Of BasePlayerSeason)
        Dim season As New BasePlayerSeason(Me.Year - 1)
        Dim playerTeamSeasons As New List(Of BasePlayerTeamSeason) From {
            {New BasePlayerTeamSeason(Me.Year - 1, Me.pts1)},
            {New BasePlayerTeamSeason(Me.Year, Me.pts1)}
        }
        season.AddPlayerTeamSeasons(playerTeamSeasons)
        seasons.Add(season)
        season = New BasePlayerSeason(Me.Year)
        playerTeamSeasons = New List(Of BasePlayerTeamSeason) From {
            {New BasePlayerTeamSeason(Me.Year, Me.pts1)},
            {New BasePlayerTeamSeason(Me.Year, Me.pts1)}
        }
        season.AddPlayerTeamSeasons(playerTeamSeasons)
        seasons.Add(season)
        Return seasons
    End Function

End Class