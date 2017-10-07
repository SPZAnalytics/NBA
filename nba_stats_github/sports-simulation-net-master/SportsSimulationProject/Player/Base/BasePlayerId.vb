Option Strict On

Namespace Player
    Namespace Base
        Public Class BasePlayerId

            ''' <summary>
            ''' Gets or sets the id.
            ''' </summary>
            ''' <value>String representing Id.</value>
            Public Property Id() As String
            ''' <summary>
            ''' Gets or sets the source.
            ''' </summary>
            ''' <value>The source of the Id value.</value>
            Public Property Source() As String

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerId" /> class.
            ''' </summary>
            Public Sub New()

            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerId" /> class.
            ''' </summary>
            ''' <param name="id">The id.</param>
            ''' <param name="source">The source.</param>
            Public Sub New(ByVal id As String, ByVal source As String)
                Me.Id = id
                Me.Source = source
            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerId" /> class.
            ''' </summary>
            ''' <param name="pid">Dictionary with id and source strings.</param>
            Public Sub New(ByVal pid As Dictionary(Of String, String))
                Me.Id = pid.Keys(0)
                Me.Source = pid.Values(0)
            End Sub
        End Class
    End Namespace
End Namespace