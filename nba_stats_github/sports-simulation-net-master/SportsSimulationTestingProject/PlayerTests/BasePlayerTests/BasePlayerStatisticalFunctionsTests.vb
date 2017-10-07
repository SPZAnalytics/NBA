Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base

<TestFixture()> _
Public Class BasePlayerStatisticalFunctionsTests

    Public Property PlayerTeamSeason As BasePlayerTeamSeason
    Public Property StatFunctions As BasePlayerStatisticalFunctions
    Public Property Stats As Dictionary(Of String, Object)
    Public Property Year As Integer = 2006

    <SetUp()> _
    Public Sub SetUp()
        Me.Stats = New Dictionary(Of String, Object) From {
            {"Minutes", 2000},
            {"Games", 72},
            {"Points", 2100},
            {"Rebounds", 800}
        }
        Me.PlayerTeamSeason = (New BasePlayerTeamSeason(Me.Stats))
    End Sub
    <TearDown()> _
    Public Sub TearDown()
        'nothing to go here
    End Sub

    <Test()> _
    Public Sub New_NoParameters_ReturnsTrue()
        Me.StatFunctions = BasePlayerStatisticalFunctions.Instance
        Assert.NotNull(Me.StatFunctions, "Variable is not instance of class")
    End Sub

    <Test()> _
    Public Sub PerGame_ValidTotalAndGamesPlayed_ReturnsTrue()
        Dim total As Integer = 2000
        Dim gp As Integer = 82
        Dim ppg As Double = total / gp
        Assert.AreEqual(Me.StatFunctions.PerGame(total, gp), ppg, "ppg not equal")
    End Sub

    <Test()> _
    Public Sub PerGame_LookupTotalAndGamesPlayed_ReturnsTrue()
        Dim objtotal As Object = 2100
        Dim objgp As Object = 72
        Dim total As Integer = CInt(Me.PlayerTeamSeason.GetStat("Points"))
        Dim gp As Integer = CInt(Me.PlayerTeamSeason.GetStat("Games"))
        Dim ppg As Double = CInt(objtotal) / CInt(objgp)
        Assert.AreEqual(Me.StatFunctions.PerGame(total, gp), ppg, "ppg not equal")
    End Sub

    <Test()> _
    Public Sub PerTimePeriod_ValidTotalAndMinutes_ReturnsTrue()
        Dim total As Integer = 2100
        Dim min As Integer = 2000
        Dim timeperiod As Integer = 40
        Dim pp40 As Double = total / min * timeperiod
        Assert.AreEqual(Me.StatFunctions.PerTimePeriod(CInt(Me.PlayerTeamSeason.GetStat("Points")), CInt(Me.PlayerTeamSeason.GetStat("Minutes")), 40), pp40, "pp40 not equal")
    End Sub

    <Test()> _
    Public Sub PerTimePeriod_LookupTotalAndMinutes_ReturnsTrue()
        Dim objtotal As Object = Me.PlayerTeamSeason.GetStat("Points")
        Dim objmin As Object = Me.PlayerTeamSeason.GetStat("Minutes")
        Dim timeperiod As Integer = 40
        Dim pp40 As Double = CInt(objtotal) / CInt(objmin) * timeperiod
        Assert.AreEqual(Me.StatFunctions.PerTimePeriod(CInt(Me.PlayerTeamSeason.GetStat("Points")), CInt(Me.PlayerTeamSeason.GetStat("Minutes")), 40), pp40, "pp40 not equal")
    End Sub

End Class