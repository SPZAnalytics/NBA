Option Strict On

Namespace Player
    Namespace Base
        Public Class BasePlayerSeason

            ''' <summary>
            ''' Gets or sets the year.
            ''' </summary>
            ''' <value>Integer representing season year.</value>
            ''' <remarks>Should error check that BasePlayerTeamSeasons.Year is equal to this value.</remarks>
            Public Property Year() As Integer
            ''' <summary>
            ''' Gets or sets the player team seasons.
            ''' </summary>
            ''' <value>List of BasePlayerTeamSeason objects.</value>
            Public Property PlayerTeamSeasons As List(Of BasePlayerTeamSeason)
            
            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerSeason" /> class.
            ''' </summary>
            ''' <remarks>Sets PlayerTeamSeasons property to empty list.</remarks>
            Public Sub New()
                Me.PlayerTeamSeasons = New List(Of BasePlayerTeamSeason)
            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerSeason" /> class.
            ''' </summary>
            ''' <param name="year">Integer representing the season year.</param>
            Public Sub New(ByVal year As Integer)
                Me.PlayerTeamSeasons = New List(Of BasePlayerTeamSeason)
                Me.Year = year
            End Sub

            ' public methods
            ''' <summary>
            ''' Adds BasePlayerTeamSeason to List of BasePlayerTeamSeason
            ''' </summary>
            ''' <param name="teamSeason"><see cref="BasePlayerTeamSeason"></see> to add.</param>
            Public Sub AddPlayerTeamSeason(ByVal teamSeason As BasePlayerTeamSeason)
                Me.PlayerTeamSeasons.Add(teamSeason)
            End Sub

            ''' <summary>
            ''' Adds List of BasePlayerTeamSeason to existing List of BasePlayerTeamSeason
            ''' </summary>
            ''' <param name="teamSeasons">List of <see cref="BasePlayerTeamSeason"></see> to add.</param>
            Public Sub AddPlayerTeamSeasons(ByVal teamSeasons As List(Of BasePlayerTeamSeason))
                For Each teamSeason As BasePlayerTeamSeason In teamSeasons
                    Me.AddPlayerTeamSeason(teamSeason)
                Next
            End Sub

            ''' <summary>
            ''' Gets the season total for a particular statistic.
            ''' </summary>
            ''' <param name="statname">String representing statistic name.</param>
            ''' <returns>Sum of stat from BasePlayerTeamSeason in list.</returns>
            Public Function GetSeasonTotal(ByVal statname As String) As Double
                Dim total As Double = 0
                For Each seas As BasePlayerTeamSeason In Me.PlayerTeamSeasons
                    Dim stat As Double = CDbl(seas.GetStat(statname))
                    total += stat
                Next
                Return total
            End Function

            ''' <summary>
            ''' Numbers BasePlayerTeamSeason objects in list.
            ''' </summary>
            ''' <returns>Integer</returns>
            Public Function NumberOfBasePlayerTeamSeasons() As Integer
                Dim num As Integer = 0
                For Each season As BasePlayerTeamSeason In Me.PlayerTeamSeasons
                    num += 1
                Next
                Return (num)
            End Function

        End Class
    End Namespace
End Namespace