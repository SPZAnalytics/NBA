Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base

Namespace PlayerTests
    Namespace Base

        <TestFixture()> _
        Public Class BasePlayerIdTests

            <SetUp()> _
            Public Sub SetUp()

            End Sub
            <TearDown()> _
            Public Sub TearDown()
                'nothing to go here
            End Sub

            <Test()> _
            Public Sub New_NoParameters_ReturnsTrue()
                Dim id As String = "ABDULKA01"
                Dim source As String = "basketball-reference.com"
                Dim pid As New BasePlayerId()
                pid.Id = id
                pid.Source = source
                Assert.AreSame(id, pid.Id, "Ids not the same")
                Assert.AreSame(source, pid.Source, "Sources not the same")
            End Sub

            <Test()> _
            Public Sub New_ValidParameters_ReturnsTrue()
                Dim id As String = "ABDULKA01"
                Dim source As String = "basketball-reference.com"
                Dim pid As New BasePlayerId(id, source)
                Assert.AreSame(id, pid.Id, "Ids not the same")
                Assert.AreSame(source, pid.Source, "Sources not the same")
            End Sub

            <Test()> _
            Public Sub New_ValidHash_ReturnsTrue()
                Dim data As New Dictionary(Of String, String) From {{"ADBULKA01", "basketball-reference.com"}}
                Dim pid As New BasePlayerId(data)
                Assert.AreSame(data.Keys(0), pid.Id, "Ids not the same")
                Assert.AreSame(data.Values(0), pid.Source, "Sources not the same")
            End Sub

        End Class
    End Namespace
End Namespace