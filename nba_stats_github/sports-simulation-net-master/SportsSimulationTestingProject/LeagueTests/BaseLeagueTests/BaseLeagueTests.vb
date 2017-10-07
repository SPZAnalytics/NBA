Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base
Imports SportsSimulation.Team.Base
Imports SportsSimulation.League.Base
Imports SportsSimulationTesting.PlayerTests.Base
Imports SportsSimulationTesting.TeamTests.Base

Namespace LeagueTests
    Namespace Base

        <TestFixture()> _
        Public Class BaseLeagueTests

            Public Property PlayerHelpers As BasePlayerTestHelpers
            Public Property Players As List(Of BasePlayer)
            Public Property League As BaseLeague

            <SetUp()> _
            Public Sub SetUp()
                Me.Players = New List(Of BasePlayer)
                Me.PlayerHelpers = New BasePlayerTestHelpers()
                Me.League = New BaseLeague(New List(Of String) From {"Points", "Minutes", "Rebounds"})
            End Sub

            <TearDown()> _
            Public Sub TearDown()
                'nothing to go here
            End Sub

            ' start tests

            <Test()> _
            Public Sub New_NoParameter_ReturnsTrue()
                Assert.IsFalse(Me.League Is Nothing, "Team constructor failed")
            End Sub

            <Test()> _
            Public Sub AddPlayer_ValidPlayer_ReturnsTrue()
                Dim player As New BasePlayer
                Me.League.AddPlayer(player)
                Assert.AreEqual(1, Me.League.Players.Count, "Did not successfully add player.")
            End Sub

            <Test()> _
            Public Sub AddPlayers_ValidPlayers_ReturnsTrue()
                Me.League.AddPlayers(New List(Of BasePlayer) From {{New BasePlayer}, {New BasePlayer}})
                Assert.AreEqual(2, Me.League.Players.Count, "Did not successfully add player.")
            End Sub

            <Test()> _
            Public Sub AddTeam_ValidTeam_ReturnsTrue()
                Dim team As New BaseTeam
                Me.League.AddTeam(team)
                Assert.AreEqual(1, Me.League.Teams.Count, "Did not successfully add team.")
            End Sub

            <Test()> _
            Public Sub AddTeams_ValidTeams_ReturnsTrue()
                Dim teams As New List(Of BaseTeam) From {New BaseTeam, New BaseTeam}
                Me.League.AddTeams(teams)
                Assert.AreEqual(2, Me.League.Teams.Count, "Did not successfully add team.")
            End Sub

        End Class

    End Namespace
End Namespace