Option Strict On

Imports SportsSimulation.Player.Base

Namespace Team
    Namespace Base
        ''' <summary>
        ''' Right now a container for BasePlayer objects, with some aggregation features.
        ''' </summary>
        Public Class BaseTeam

            ''' <summary>
            ''' Gets or sets the games lost.
            ''' </summary>
            ''' <value>The team's games lost.</value>
            Public Property GamesLost As Integer
            ''' <summary>
            ''' Gets or sets the games won.
            ''' </summary>
            ''' <value>The team's games won.</value>
            Public Property GamesWon As Integer
            ''' <summary>
            ''' Gets or sets the team id.
            ''' </summary>
            ''' <value>The team's id.</value>
            Public Property Id As String
            ''' <summary>
            ''' Gets or sets the league id.
            ''' </summary>
            ''' <value>The league's id.</value>
            Public Property LeagueId As String
            ''' <summary>
            ''' Gets or sets list of players.
            ''' </summary>
            ''' <value><see cref="List(of BasePlayer)"></see></value>
            Public Property Players() As List(Of BasePlayer)
            ''' <summary>
            ''' Gets or sets the points allowed.
            ''' </summary>
            ''' <value>The points allowed by the team.</value>
            Public Property PointsAllowed As Integer
            ''' <summary>
            ''' Gets or sets the points scored.
            ''' </summary>
            ''' <value>The points scored by the team.</value>
            Public Property PointsScored As Integer
            ''' <summary>
            ''' Need list of stat categories to perform team aggregate calculations.
            ''' </summary>
            ''' <value>List of stat categories.</value>
            Public Property StatCategories As List(Of String)

            ' public methods
            ''' <summary>
            ''' Initializes a new instance of the <see cref="BaseTeam" /> class.
            ''' </summary>
            Public Sub New()
                Me.Players = New List(Of BasePlayer)
                Me.StatCategories = New List(Of String)
            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BaseTeam" /> class.
            ''' </summary>
            ''' <param name="statCategories">List of stat categories.</param>
            ''' <remarks>Chose flexible implementation where can choose what stats matter. If need rigid list, 
            ''' then can subclass and use constant instead of permitting assignment when creating object.</remarks>
            Public Sub New(ByVal statCategories As List(Of String))
                Me.Players = New List(Of BasePlayer)
                Me.StatCategories = statCategories
            End Sub

            ''' <summary>
            ''' Adds player to list of players.
            ''' </summary>
            ''' <param name="player"><see cref="BasePlayer"></see></param>
            Public Sub AddPlayer(ByVal player As BasePlayer)
                Me.Players.Add(player)
            End Sub

            ''' <summary>
            ''' Adds list of players to existing list of players.
            ''' </summary>
            ''' <param name="players"><see cref="List(of BasePlayer)"></see></param>
            Public Sub AddPlayers(ByVal players As List(Of BasePlayer))
                For Each bp As BasePlayer In players
                    Me.AddPlayer(bp)
                Next
            End Sub

            ''' <summary>
            ''' Creates dictionary of statname and team totals by looping through each stat category.
            ''' </summary>
            ''' <param name="players">List of players.</param>
            ''' <param name="year">Season year.</param>
            ''' <returns>Dictionary of statname and team totals.</returns>
            Public Function AllTeamStatsTotals(ByVal players As List(Of BasePlayer), ByVal year As Integer) As Dictionary(Of String, Double)
                Dim teamStatTotals As New Dictionary(Of String, Double)
                For Each statCategory As String In Me.StatCategories
                    Dim tot As Double = 0
                    Try
                        tot = Me.TeamStatTotal(players, statCategory, year)
                    Catch ex As Exception
                    End Try
                    teamStatTotals.Add(statCategory, tot)
                Next
                Return teamStatTotals
            End Function

            ''' <summary>
            ''' Gets the player by id.
            ''' </summary>
            ''' <param name="id">The id string.</param>
            ''' <returns><see cref="BasePlayer"></see> if player with id exists; otherwise nothing.</returns>
            Public Function GetPlayerById(ByVal lbp As List(Of BasePlayer), ByVal id As String, ByVal source As String) As BasePlayer
                Dim player As BasePlayer = Me.QueryPlayerById(lbp, id, source)
                If player Is Nothing Then
                    Throw New Exception("Could not find player with id: " & id & vbTab & source)
                End If
                Return player
            End Function

            Public Function TeamPointDifferential() As Integer
                Return Me.PointsScored - Me.PointsAllowed
            End Function

            Public Function TeamStatAverage(ByVal lbp As List(Of BasePlayer), ByVal statname As String, ByVal year As Integer) As Double
                If lbp Is Nothing Or lbp.Count = 0 Or String.IsNullOrEmpty(statname) Or year = 0 Or year = Nothing Then
                    Throw New Exception("Cannot calculate TeamStatAverage with null or empty parameters")
                End If
                Dim tot As Double = Me.TeamStatTotal(lbp, statname, year)
                Return tot / lbp.Count
            End Function

            Public Function TeamStatPerTimePeriod(ByVal lbp As List(Of BasePlayer), ByVal statname As String, ByVal year As Integer, ByVal timePeriod As Integer) As Double
                Dim avg As Double = Me.TeamStatTotal(lbp, statname, year) / Me.TeamStatTotal(lbp, "Minutes", year) * timePeriod
                Return avg
            End Function

            ''' <summary>
            ''' Calculates team's stat total for a single stat category.
            ''' </summary>
            ''' <param name="lbp">List of players.</param>
            ''' <param name="statname">Name of statistic to total.</param>
            ''' <param name="year">The season year.</param>
            ''' <returns>Double</returns>
            Public Function TeamStatTotal(ByVal lbp As List(Of BasePlayer), ByVal statname As String, ByVal year As Integer) As Double
                Dim tot As Double = 0
                For Each bp As BasePlayer In lbp
                    Dim p As BasePlayerSeason = bp.GetSeason(year)
                    If p Is Nothing Then
                        Throw New Exception("Query did not return a BasePlayerSeason")
                    End If
                    Dim stot As Double = 0
                    Try
                        stot = p.GetSeasonTotal(statname)
                    Catch ex As Exception
                    End Try
                    If stot = 0.0 Or stot = Nothing Then
                        Throw New Exception("Season total should not be zero.")
                    End If
                    tot += stot
                Next
                Return tot
            End Function

            ''' <summary>
            ''' Determines player that leads team in particular stat.
            ''' </summary>
            ''' <param name="lbp">List of players.</param>
            ''' <param name="statname">Name of statistic to determine leader.</param>
            ''' <param name="year">The season year.</param>
            ''' <returns>BasePlayer</returns>
            Public Function TeamLeaderInStat(ByVal lbp As List(Of BasePlayer), ByVal statname As String, ByVal year As Integer) As BasePlayer
                Dim leader As New BasePlayer
                Dim leaderTotal As Double = 0
                For Each bp As BasePlayer In lbp
                    Dim p As BasePlayerSeason = bp.GetSeason(year)
                    If p Is Nothing Then
                        Throw New Exception("Query did not return a BasePlayerSeason")
                    End If
                    Dim stot As Double = 0
                    Try
                        stot = p.GetSeasonTotal(statname)
                    Catch ex As Exception
                    End Try
                    If stot = 0.0 Or stot = Nothing Then
                        Throw New Exception("Season total should not be zero.")
                    End If
                    If leaderTotal = 0 And stot > 0 Then
                        leader = bp
                        leaderTotal = stot
                    ElseIf stot >= leader.GetSeasonTotal(statname, year) Then
                        leader = bp
                        leaderTotal = stot
                    End If
                Next
                Return leader
            End Function

            Public Function TeamTrailerInStat(ByVal lbp As List(Of BasePlayer), ByVal statname As String, ByVal year As Integer) As BasePlayer
                Dim trailer As New BasePlayer
                Dim trailerTotal As Double = Nothing
                For Each bp As BasePlayer In lbp
                    Dim p As BasePlayerSeason = bp.GetSeason(year)
                    If p Is Nothing Then
                        Throw New Exception("Query did not return a BasePlayerSeason")
                    End If
                    Dim stot As Double = Nothing
                    Try
                        stot = p.GetSeasonTotal(statname)
                    Catch ex As Exception
                    End Try
                    If stot = Nothing Then
                        Throw New Exception("Season total should not be Nothing.")
                    End If
                    If trailerTotal = Nothing Or stot < trailerTotal Then
                        trailerTotal = stot
                        trailer = bp
                    End If
                Next
                Return trailer
            End Function

            Public Function TeamWinningPercentage() As Double
                Return Me.GamesWon / (Me.GamesWon + Me.GamesLost)
            End Function

            ' private methods
            Private Function QueryPlayerById(ByVal players As List(Of BasePlayer), ByVal idToMatch As String, ByVal sourceToMatch As String) As BasePlayer
                Dim query = (From bp As BasePlayer In players
                            Where bp.GetIdsAndSources.ContainsKey(idToMatch) And bp.GetIdsAndSources.ContainsValue(sourceToMatch)
                            Select bp).First
                Return query
            End Function

        End Class
    End Namespace
End Namespace