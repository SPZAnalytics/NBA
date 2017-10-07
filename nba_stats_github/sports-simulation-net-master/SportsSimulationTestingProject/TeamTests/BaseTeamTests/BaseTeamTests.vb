Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base
Imports SportsSimulation.Team.Base
Imports SportsSimulationTesting.PlayerTests.Base

Namespace TeamTests
    Namespace Base


        <TestFixture()> _
        Public Class BaseTeamTests

            Public Property PlayerHelpers As BasePlayerTestHelpers
            Public Property Players As List(Of BasePlayer)
            Public Property Team As BaseTeam

            <SetUp()> _
            Public Sub SetUp()
                Me.Players = New List(Of BasePlayer)
                Me.PlayerHelpers = New BasePlayerTestHelpers()
                Me.Team = New BaseTeam(New List(Of String) From {"Points", "Minutes", "Rebounds"})
            End Sub

            <TearDown()> _
            Public Sub TearDown()
                'nothing to go here
            End Sub

            ' start tests

            <Test()> _
            Public Sub New_NoParameter_ReturnsTrue()
                Assert.IsFalse(Me.Team Is Nothing, "Team constructor failed")
            End Sub

            <Test()> _
            Public Sub Players_NoParameter_ReturnsTrue()
                Dim players As List(Of BasePlayer) = Me.Team.Players
                Assert.IsFalse(players Is Nothing, "Players initialization failed")
            End Sub

            <Test()> _
            Public Sub AddPlayer_ValidPlayer_ReturnsTrue()
                Dim player As New BasePlayer
                Me.Team.AddPlayer(player)
                Assert.AreEqual(1, Me.Team.Players.Count, "Did not successfully add player.")
            End Sub

            <Test()> _
            Public Sub AddPlayers_ValidPlayers_ReturnsTrue()
                Me.Team.AddPlayers(New List(Of BasePlayer) From {{New BasePlayer}, {New BasePlayer}})
                Assert.AreEqual(2, Me.Team.Players.Count, "Did not successfully add player.")
            End Sub

            <Test()> _
            Public Sub TeamStatTotal_ValidStatname_ReturnsTrue()
                Me.Team.AddPlayers(Me.PlayerHelpers.CreatePlayersWithStats)
                ' test that added players
                Assert.AreEqual(Me.PlayerHelpers.Ids.Count, Me.Team.Players.Count, "Did not successfully add player.")
                ' now test totals
                Dim statName As String = "Points"
                Dim statTotal As Double = 0
                Try
                    statTotal = Me.Team.TeamStatTotal(Me.Team.Players, "Points", Me.PlayerHelpers.Year)
                Catch ex As Exception
                End Try
                Assert.AreEqual(Me.PlayerHelpers.Year * Me.PlayerHelpers.Ids.Count * 2, statTotal, "Stat total should be 4X year (2 players, 2 team seasons).")
            End Sub

            <Test()> _
            Public Sub TeamLeader_ValidStatname_ReturnsTrue()
                Me.AddPlayersToTeam()
                ' now test totals
                Dim statName As String = "Points"
                Dim leader As BasePlayer = Me.Team.TeamLeaderInStat(Me.Players, statName, Me.PlayerHelpers.Year)
                Dim season As BasePlayerSeason = Me.Team.Players(0).GetSeason(Me.PlayerHelpers.Year)
                Dim tot As Double = season.GetSeasonTotal(statName)
                Assert.AreEqual(Me.PlayerHelpers.Year * 2, tot, "Points should be 2X year (2 playerteamseasons).")
            End Sub

            <Test()> _
            Public Sub AllTeamStatsTotals_NoParameters_ReturnsTrue()
                Me.AddPlayersToTeam()
                Dim allTeamStats As New Dictionary(Of String, Double)
                allTeamStats = Me.Team.AllTeamStatsTotals(Me.Team.Players, Me.PlayerHelpers.Year)
                Dim expectedTotal As Double = Me.PlayerHelpers.Year * Me.PlayerHelpers.Ids.Count * 2
                Dim actualTotal As Double = 0
                Try
                    actualTotal = allTeamStats("Points")
                Catch ex As Exception
                    ' do nothing
                End Try
                Assert.AreEqual(expectedTotal, actualTotal, "Points total not the same.")
            End Sub

            <Test()> _
            Public Sub GetPlayerById_ValidPlayers_ReturnsTrue()
                Dim id As String = "ALLENRA01"
                Dim source As String = "basketball-reference.com"
                Me.AddPlayersToTeam()
                Dim player As BasePlayer = Me.Team.GetPlayerById(Me.Team.Players, id, source)
                Assert.AreEqual(id, player.Ids(0).Id, "Player ids not the same")
                Assert.AreEqual(source, player.Ids(0).Source, "Player sources not the same")
                id = "ABDULKA01"
                player = Me.Team.GetPlayerById(Me.Team.Players, id, source)
                Assert.AreEqual(id, player.Ids(0).Id, "Player ids not the same")
                Assert.AreEqual(source, player.Ids(0).Source, "Player sources not the same")
            End Sub

            <Test()> _
            Public Sub TeamTrailer_ValidStatname_ReturnsTrue()
                Me.AddPlayersToTeam()
                ' now test totals
                Dim statName As String = "Points"
                Dim trailer As BasePlayer = Me.Team.TeamTrailerInStat(Me.Players, statName, Me.PlayerHelpers.Year)
                Dim season As BasePlayerSeason = Me.Team.Players(0).GetSeason(Me.PlayerHelpers.Year)
                Dim tot As Double = season.GetSeasonTotal(statName)
                Assert.AreEqual(Me.PlayerHelpers.Year * 2, tot, "Points should be 2X year (2 playerteamseasons).")
            End Sub

            <Test()> _
            Public Sub TeamStatAverage_NoParameters_ReturnsTrue()
                Me.AddPlayersToTeam()
                Dim statName As String = "Points"
                Dim avg As Double = Me.Team.TeamStatAverage(Me.Team.Players, statName, Me.PlayerHelpers.Year)
                Assert.IsFalse(avg = 0, "Average should not be zero.")
                Assert.AreEqual(CDbl(Me.PlayerHelpers.Stats("Points")) * 2, avg, "Averages should not be the same.")
            End Sub

            <Test()> _
            Public Sub TeamStatPerTimePeriod_NoParameters_ReturnsTrue()
                Me.AddPlayersToTeam()
                Dim statName As String = "Points"
                Dim timePeriod As Integer = 40
                Dim avg As Double = Me.Team.TeamStatPerTimePeriod(Me.Team.Players, statName, Me.PlayerHelpers.Year, timePeriod)
                Assert.IsFalse(avg = 0, "Average should not be zero.")
                Assert.AreEqual(CDbl(Me.PlayerHelpers.Stats("Points")) / CDbl(Me.PlayerHelpers.Stats("Minutes")) * timePeriod, avg, "Averages should not be the same.")
            End Sub

            <Test()> _
            Public Sub TeamPointDifferential_NoParameters_ReturnsTrue()
                Me.Team.PointsAllowed = 100
                Me.Team.PointsScored = 50
                Assert.AreEqual(-50, Me.Team.TeamPointDifferential, "Point differentials are not the same.")
            End Sub

            <Test()> _
            Public Sub TeamWinningPercentage_NoParameters_ReturnsTrue()
                Me.Team.GamesWon = 40
                Me.Team.GamesLost = 40
                Assert.AreEqual(0.5, Me.Team.TeamWinningPercentage, "Winning percentages are not the same.")
            End Sub

            ' private methods
            Private Sub AddPlayersToTeam()
                ' add players to team
                Me.Team.AddPlayers(Me.PlayerHelpers.CreatePlayersWithStats)
            End Sub

        End Class

    End Namespace
End Namespace