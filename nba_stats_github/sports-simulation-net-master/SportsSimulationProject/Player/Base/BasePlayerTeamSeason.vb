Option Strict On

Namespace Player
    Namespace Base
        Public Class BasePlayerTeamSeason

            ''' <summary>
            ''' Gets or sets the player stats.
            ''' </summary>
            ''' <value>Stats dictionary.</value>
            Public Property Stats As Dictionary(Of String, Object)
            ''' <summary>
            ''' Gets or sets the year of the season.
            ''' </summary>
            ''' <value>The year.</value>
            Public Property Year As Integer

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerTeamSeason" /> class.
            ''' </summary>
            Public Sub New()

            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerTeamSeason" /> class.
            ''' </summary>
            ''' <param name="year">The year.</param>
            Public Sub New(ByVal year As Integer)
                Me.Year = year
            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerTeamSeason" /> class.
            ''' </summary>
            ''' <param name="stats">The statistics.</param>
            Public Sub New(ByVal stats As Dictionary(Of String, Object))
                Me.Stats = stats
            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerTeamSeason" /> class.
            ''' </summary>
            ''' <param name="year">The year.</param>
            ''' <param name="stats">The statistics.</param>
            Public Sub New(ByVal year As Integer, ByVal stats As Dictionary(Of String, Object))
                Me.Year = year
                Me.Stats = stats
            End Sub

            ' public methods
            ''' <summary>
            ''' Adds a statistic to statistics dictionary.
            ''' </summary>
            ''' <param name="n">The name of the statistic.</param>
            ''' <param name="v">The value.</param>
            Public Sub AddStat(ByVal n As String, ByVal v As Object)
                Me.Stats.Add(n, v)
            End Sub

            ''' <summary>
            ''' Adds multiple statistics to statistics dictionary.
            ''' </summary>
            ''' <param name="stats">The statistics dictionary.</param>
            Public Sub AddStats(ByVal stats As Dictionary(Of String, Object))
                For Each kvp As KeyValuePair(Of String, Object) In stats
                    Me.AddStat(kvp.Key, kvp.Value)
                Next
            End Sub

            ''' <summary>
            ''' Gets an individual stat from a team season.
            ''' </summary>
            ''' <param name="statname">The statistic name.</param>
            ''' <returns>Object</returns>
            Public Function GetStat(ByVal statname As String) As Object
                Return Me.Stats(statname)
            End Function

        End Class
    End Namespace
End Namespace