Option Strict On

Imports SportsSimulation.Player.Base

Namespace Player
    Namespace Basketball
        Public Class BasketballPlayerTeamSeason
            Inherits BasePlayerTeamSeason

            Public Sub New()
                MyBase.New()
            End Sub

            Public Sub New(ByVal year As Integer)
                MyBase.New(year)
            End Sub

            Public Sub New(ByVal stats As Dictionary(Of String, Object))
                MyBase.New(stats)
            End Sub

            Public Sub New(ByVal year As Integer, ByVal stats As Dictionary(Of String, Object))
                MyBase.New(year, stats)
            End Sub

            ' public methods
            
            ' private methods

        End Class
    End Namespace
End Namespace