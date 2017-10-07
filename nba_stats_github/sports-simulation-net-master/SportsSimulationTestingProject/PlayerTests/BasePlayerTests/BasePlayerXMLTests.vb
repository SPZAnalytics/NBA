Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base
Imports System.IO

Namespace PlayerTests
    Namespace Base

        <TestFixture()> _
        Public Class BasePlayerXMLTests

            Public Property ID As String
            Public Property PlayerXML As BasePlayerXML

            <SetUp()> _
            Public Sub SetUp()
                Me.ID = "ALLENRA01"
                Me.PlayerXML = New BasePlayerXML
            End Sub

            <TearDown()> _
            Public Sub TearDown()
                'nothing to go here
            End Sub

            ' start tests

            <Test()> _
            Public Sub New_NoParameter_ReturnsTrue()
                Assert.IsFalse(Me.PlayerXML Is Nothing, "Player constructor failed")
            End Sub

            <Test()> _
            Public Sub LoadBioFromXML_ValidParameters_ReturnsTrue()
                Dim fn As String = "C:\Users\sansbacon\Documents\Visual Studio 2010\Projects\sportssimulation\trunk\SportsSimulationTestingProject\PlayerTests\BasePlayerTests\SamplePlayers.xml"
                Dim player As BasePlayer = Me.PlayerXML.LoadBioFromXML(fn, Me.ID)
                Assert.AreEqual("Ray", player.FirstName, "First names did not match.")
            End Sub

            <Test()> _
            Public Sub LoadStatsFromXML_ValidParameters_ReturnsTrue()
                Dim fn As String = "C:\Users\sansbacon\Documents\Visual Studio 2010\Projects\sportssimulation\trunk\SportsSimulationTestingProject\PlayerTests\BasePlayerTests\SamplePlayerStats.xml"
                Dim player As BasePlayer = Me.PlayerXML.LoadStatsFromXML(fn, Me.ID)
                Dim year As Integer = 2010
                Assert.AreEqual(2, player.Seasons.Count, "Number of seasons not the same.")
                Assert.AreEqual(year * 2, player.GetSeasonTotal("Points", year), "Point totals did not match.")
            End Sub

        End Class
    End Namespace
End Namespace