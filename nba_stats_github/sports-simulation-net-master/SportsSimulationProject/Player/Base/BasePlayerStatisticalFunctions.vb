Option Strict On

Namespace Player
    Namespace Base
        Public Class BasePlayerStatisticalFunctions

            ''' <summary>
            ''' Private variable implementing Singleton pattern
            ''' </summary>
            Private Shared _Instance As BasePlayerStatisticalFunctions = Nothing

            ''' <summary>
            ''' Singleton pattern: Gets or instantiates <see cref="BasePlayerStatisticalFunctions"></see> object.
            ''' </summary>
            ''' <value>Instance of object.</value>
            Public Shared ReadOnly Property Instance() As BasePlayerStatisticalFunctions
                Get
                    If (_Instance Is Nothing) Then
                        _Instance = New BasePlayerStatisticalFunctions()
                    End If

                    Return _Instance
                End Get
            End Property

            ''' <summary>
            ''' Calculates per game statistic given games played and stat total.
            ''' </summary>
            ''' <param name="total">The stat total.</param>
            ''' <param name="gp">The games played.</param>
            ''' <returns>Double</returns>
            Public Function PerGame(ByVal total As Integer, ByVal gp As Integer) As Double
                If gp > 0 Then
                    Return total / gp
                Else
                    Return 0
                End If
            End Function

            ''' <summary>
            ''' Calculates per XX minutes statistic given minutes played, stat total, and timeperiod.
            ''' </summary>
            ''' <param name="total">The stat total.</param>
            ''' <param name="min">The minutes played.</param>
            ''' <param name="timeperiod">The timeperiod used for calculation.</param>
            ''' <returns>Double</returns>
            Public Function PerTimePeriod(ByVal total As Integer, ByVal min As Integer, ByVal timeperiod As Integer) As Double
                If min > 0 Then
                    Return total / min * timeperiod
                Else
                    Return 0
                End If
            End Function

            Private Sub New()

            End Sub

        End Class
    End Namespace
End Namespace