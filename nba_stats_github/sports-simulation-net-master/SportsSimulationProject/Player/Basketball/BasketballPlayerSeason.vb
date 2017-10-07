Option Strict On

Imports SportsSimulation.Player.Base

Namespace Player
    Namespace Basketball
        Public Class BasketballPlayerSeason
            Inherits BasePlayerSeason

            Public Sub New()
                MyBase.New()
            End Sub

            Public Sub New(ByVal year As Integer)
                MyBase.New(year)
            End Sub

        End Class
    End Namespace
End Namespace