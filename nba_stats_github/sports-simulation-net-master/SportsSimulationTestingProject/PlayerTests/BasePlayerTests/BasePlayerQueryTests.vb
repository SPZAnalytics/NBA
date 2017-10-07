Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base

Namespace PlayerTests
    Namespace Base

        <TestFixture()> _
        Public Class BasePlayerQueryTests

            Public Property Helpers As BasePlayerTestHelpers
            Public Property PlayerSeason As BasePlayerSeason
            Public Property Seasons As List(Of BasePlayerSeason)
            Public Property Stats As Dictionary(Of String, Object)
            Public Property Year As Integer

            <SetUp()> _
            Public Sub SetUp()
                Me.Helpers = New BasePlayerTestHelpers
            End Sub

            <TearDown()> _
            Public Sub TearDown()
                'nothing to go here
            End Sub

            ' start tests
            ' Public Function QuerySeason(ByVal seasons As List(Of BasePlayerSeason), ByVal year As Integer) As BasePlayerSeason
            ' Public Function QuerySeasons(ByVal s As List(Of BasePlayerSeason), ByVal year1 As Integer, ByVal year2 As Integer) As List(Of BasePlayerSeason)

            <Test()> _
            Public Sub Instance_NoParameter_ReturnsTrue()
                Dim bpq As BasePlayerQuery = BasePlayerQuery.Instance
                Assert.IsFalse(bpq Is Nothing, "Instance property failed")
            End Sub

            <Test()> _
            Public Sub QuerySeason_ValidParameters_ReturnsTrue()
                Dim player As New BasePlayer
                player.Seasons = Me.Helpers.CreateSeasonsWithStats
                Dim bpq As BasePlayerQuery = BasePlayerQuery.Instance
                Dim qSeason As BasePlayerSeason = bpq.QuerySeason(player.Seasons, Me.Helpers.Year - 1)
                Assert.AreEqual(qSeason, player.Seasons(0), "Seasons 1 are not equal.")
            End Sub

            <Test()> _
            Public Sub QuerySeasons_ValidParameters_ReturnsTrue()
                Dim player As New BasePlayer
                player.Seasons = Me.Helpers.CreateSeasonsWithStats
                Dim bpq As BasePlayerQuery = BasePlayerQuery.Instance
                Dim qSeasons As List(Of BasePlayerSeason) = bpq.QuerySeasons(player.Seasons, Me.Helpers.Year - 1, Me.Helpers.Year)
                Assert.AreEqual(qSeasons.Count, player.Seasons.Count, "Number of seasons are not the same.")
                Assert.AreEqual(qSeasons(0), player.Seasons(0), "Seasons 1 are not equal.")
            End Sub

        End Class
    End Namespace
End Namespace