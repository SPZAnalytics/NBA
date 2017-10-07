'Option Strict On

'Imports NUnit.Framework
'Imports SportsSimulation.Player.Basketball

'<TestFixture()> _
'Public Class BasketballPlayerSeasonTests

'    'Public Class BasePlayerSeason
'    '    Public Property Stats() As Dictionary(Of String, Object)
'    '    Public Function PerGame(ByVal total As Integer, ByVal gp As Integer) As Double
'    '    Public Function PerTimePeriod(ByVal total As Integer, ByVal min As Integer, ByVal timeperiod As Integer) As Double

'    Public Property PlayerSeason As BasePlayerSeason
'    Public Property Stats As Dictionary(Of String, Object)
'    Public Property pts1 As Dictionary(Of String, Object)

'    <SetUp()> _
'    Public Sub SetUp()
'        Me.PlayerSeason = New BasePlayerSeason()
'        pts1 = New Dictionary(Of String, Object) From {
'                    {"Minutes", 1100},
'                    {"Games", 40},
'                    {"Points", 1100},
'                    {"Rebounds", 40}
'                }
'    End Sub
'    <TearDown()> _
'    Public Sub TearDown()
'        'nothing to go here
'    End Sub

'    <Test()> _
'    Public Sub Stats_ValidMinutes_ReturnsTrue()
'        Me.PlayerSeason.Stats = pts1
'        Assert.AreEqual(Me.PlayerSeason.Stats("Minutes"), 1100, "stats are not the same.")
'    End Sub

'    <Test()> _
'    Public Sub Stats_ValidPoints_ReturnsTrue()
'        Me.PlayerSeason.Stats = pts1
'        Assert.AreEqual(Me.PlayerSeason.Stats("Points"), 1100, "stats are not the same.")
'    End Sub

'    <Test()> _
'    Public Sub PerGame_ValidTotalAndGamesPlayed_ReturnsTrue()
'        Me.PlayerSeason.Stats = pts1
'        Dim actualTotal As Integer = 1100
'        Dim actualGp As Integer = 40
'        Dim ppg As Double = actualTotal / actualGp
'        Dim total As Integer = CInt(Me.PlayerSeason.Stats("Points"))
'        Dim gp As Integer = CInt(Me.PlayerSeason.Stats("Games"))
'        Assert.AreEqual(ppg, Me.PlayerSeason.PerGame(actualTotal, actualGp), "ppg not equal")
'    End Sub

'    <Test()> _
'    Public Sub PerTimePeriod_ValidTotalAndMinutes_ReturnsTrue()
'        Me.PlayerSeason.Stats = pts1
'        Dim actualTotal As Integer = 1100
'        Dim actualMin As Integer = 1100
'        Dim timeperiod As Integer = 40
'        Dim actualPp40 As Double = actualTotal / actualMin * timeperiod
'        Dim expectedTotal As Integer = CInt(Me.PlayerSeason.Stats("Points"))
'        Dim expectedMin As Integer = CInt(Me.PlayerSeason.Stats("Minutes"))
'        Assert.AreEqual(Me.PlayerSeason.PerTimePeriod(expectedTotal, expectedMin, 40), actualPp40, "pp40 not equal")
'    End Sub

'End Class